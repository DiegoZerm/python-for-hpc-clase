def test_eigensolver():
    import HelloWorld
    import numpy as np
    import numpy.linalg as LA
    N = 50
    matrix = np.random.rand(N, N)
    eigenvalues, eigenvectors = HelloWorld.eigen(matrix)
    eigenvalues_np, eigenvectors_np = LA.eig(matrix)
    assert(np.allclose(eigenvalues, eigenvalues_np))
    assert(np.allclose(eigenvectors, eigenvectors_np))
