import numpy as np

import pycuda.gpuarray as gpuarray
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
# get GPU info
#gpu = cuda.Device(0)
#print gpu.multiprocessor_count
#print gpu.max_threads_per_block
#print gpu.max_block_dim_x
#print gpu.max_block_dim_y
#print gpu.max_grid_dim_x
#print gpu.max_grid_dim_y
#print gpu.warp_size


from string import Template
code = Template("""
    #include <stdio.h>
    #include <math.h>

    /*for shuffle of double-precision point */
    __device__ __inline__ double shfl(double x, int lane)
    {
        // Split the double number into 2 32b registers.
        int lo, hi;
        asm volatile("mov.b64 {%0,%1}, %2;":"=r"(lo),"=r"(hi):"d"(x));
        // Shuffle the two 32b registers.
        lo = __shfl_down(lo,lane,warpSize);
        hi = __shfl_down(hi,lane,warpSize);
        //lo = __shfl_xor(lo,lane,warpSize);
        //hi = __shfl_xor(hi,lane,warpSize);
        // Recreate the 64b number.
        asm volatile("mov.b64 %0,{%1,%2};":"=d"(x):"r"(lo),"r"(hi));
        return x;
    }

    /*for shuffle of long long */

    __device__ __inline__ double atomicAdd_d(double* address, double val)
    {
        unsigned long long int* address_as_ull =
                                              (unsigned long long int*)address;
        unsigned long long int old = *address_as_ull, assumed;
        do {
            assumed = old;
            old = atomicCAS(address_as_ull, assumed, 
                            __double_as_longlong(val + 
                            __longlong_as_double(assumed)));
        } while (assumed != old);
        return __longlong_as_double(old);
    }

    __inline__ __device__
    unsigned long long int warpReduceSum(unsigned long long int val) {
      for (int mask = warpSize/2; mask > 0; mask /= 2) 
        //val += __shfl_down(val, mask);
        val += (unsigned long long int)shfl((double)val, mask);
      return val;
    }

    __inline__ __device__
    unsigned long long int blockReduceSum(unsigned long long int val) {

      static __shared__ int shared[32]; // Shared mem for 32 partial sums
      int lane = threadIdx.x % warpSize;
      int wid = threadIdx.x / warpSize;

      val = warpReduceSum(val);     // Each warp performs partial reduction


      if (lane==0) shared[wid]=val; // Write reduced value to shared memory

      __syncthreads();              // Wait for all partial reductions

      //read from shared memory only if that warp existed
      val = (threadIdx.x < blockDim.x / warpSize) ? shared[lane] : 0;

      if (wid==0) val = warpReduceSum(val); //Final reduce within first warp

      return val;
    }

    __inline__ __device__
    double warpReduceSumf(double val) {
      for (int mask = warpSize/2; mask > 0; mask /= 2) 
        //val += __shfl_down(val, mask);
        val += shfl(val, mask);
      return val;
    }

    __inline__ __device__
    double blockReduceSumf(double val) {

      static __shared__ double shared[32]; // Shared mem for 32 partial sums
      int lane = threadIdx.x % warpSize;
      int wid = threadIdx.x / warpSize;

      val = warpReduceSumf(val);     // Each warp performs partial reduction


      if (lane==0) shared[wid]=val; // Write reduced value to shared memory

      __syncthreads();              // Wait for all partial reductions

      //read from shared memory only if that warp existed
      val = (threadIdx.x < blockDim.x / warpSize) ? shared[lane] : 0;

      if (wid==0) val = warpReduceSumf(val); //Final reduce within first warp

      return val;
    }


    __global__ void velcorrelation(double *pos, double *vel,
          double* real_edges, double *velcorr, unsigned long long int *numbin) 
    {
      const int npart = ${npart};
      const int nbins = ${nbins};
      double dx, dy, dz, dist;
      int i, j, k;
      unsigned long long int numbin_cache[nbins];
      double velcorr_cache[nbins*6];

      for (k = 0; k < nbins; k++)
        {
          numbin_cache[k] = 0;
          velcorr_cache[k*6+0] = 0.0;
          velcorr_cache[k*6+1] = 0.0;
          velcorr_cache[k*6+2] = 0.0;
          velcorr_cache[k*6+3] = 0.0;
          velcorr_cache[k*6+4] = 0.0;
          velcorr_cache[k*6+5] = 0.0;
        }

      for (i = blockIdx.x * blockDim.x + threadIdx.x; 
          i < npart; 
          i += blockDim.x * gridDim.x) 
        {
          //printf("T %d, B %d, i %d\\n", threadIdx.x, blockIdx.x, i);
          for (j = 0; j < i; j++)
            {
              dx = pos[j*3 + 0] - pos[i*3 + 0];
              dy = pos[j*3 + 1] - pos[i*3 + 1];
              dz = pos[j*3 + 2] - pos[i*3 + 2];

              dist = sqrt(dx*dx + dy*dy + dz*dz);
              //dist = dx*dx + dy*dy + dz*dz;
              // get bin index for dist
              for (k = 0; k < nbins; k++)
                {
                  if (dist < real_edges[k+1]) break;
                }

              numbin_cache[k] += 1;
              velcorr_cache[k*6+0] += vel[i*3 + 0] * vel[j*3 + 0];
              velcorr_cache[k*6+1] += vel[i*3 + 1] * vel[j*3 + 1];
              velcorr_cache[k*6+2] += vel[i*3 + 2] * vel[j*3 + 2];
              velcorr_cache[k*6+3] += vel[i*3 + 0] * vel[j*3 + 1];
              velcorr_cache[k*6+4] += vel[i*3 + 0] * vel[j*3 + 2];
              velcorr_cache[k*6+5] += vel[i*3 + 1] * vel[j*3 + 2];
            }
        }

      // Reducing velcorr and numbin
      for (k = 0; k < nbins; k++)
        {
          // reduce in block
          numbin_cache[k] = blockReduceSum(numbin_cache[k]);
          velcorr_cache[6*k + 0] = blockReduceSumf(velcorr_cache[6*k + 0]);
          velcorr_cache[6*k + 1] = blockReduceSumf(velcorr_cache[6*k + 1]);
          velcorr_cache[6*k + 2] = blockReduceSumf(velcorr_cache[6*k + 2]);
          velcorr_cache[6*k + 3] = blockReduceSumf(velcorr_cache[6*k + 3]);
          velcorr_cache[6*k + 4] = blockReduceSumf(velcorr_cache[6*k + 4]);
          velcorr_cache[6*k + 5] = blockReduceSumf(velcorr_cache[6*k + 5]);

          // reduce among blocks
          if (threadIdx.x == 0)
            {
              atomicAdd(&numbin[k], numbin_cache[k]);
              atomicAdd_d(&velcorr[6*k + 0], velcorr_cache[6*k + 0]);
              atomicAdd_d(&velcorr[6*k + 1], velcorr_cache[6*k + 1]);
              atomicAdd_d(&velcorr[6*k + 2], velcorr_cache[6*k + 2]);
              atomicAdd_d(&velcorr[6*k + 3], velcorr_cache[6*k + 3]);
              atomicAdd_d(&velcorr[6*k + 4], velcorr_cache[6*k + 4]);
              atomicAdd_d(&velcorr[6*k + 5], velcorr_cache[6*k + 5]);
            }
        }
    }
    """)

def velcorrelation_gpu(pos, vel, real_edges, nbins):
    npart = pos.shape[0]
    # generate code
    codefinal = code.substitute(npart="%d"%npart, nbins="%d"%nbins)
    mod = SourceModule(codefinal)
    func = mod.get_function("velcorrelation")

    # return arrays
    sumcorr = np.zeros((nbins,6), dtype=np.float64)
    numbin = np.zeros(nbins, dtype=np.int64)

    func(cuda.In(pos.astype(np.float64)), cuda.In(vel.astype(np.float64)), 
        cuda.In(real_edges.astype(np.float64)), 
        cuda.InOut(sumcorr), cuda.InOut(numbin),
        block=(512,1,1), grid=(4096,1))

    return sumcorr, numbin
