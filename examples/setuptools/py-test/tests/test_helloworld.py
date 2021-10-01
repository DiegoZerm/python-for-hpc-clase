def test_import():
    import HelloWorld

def test_helloworld_output(capsys):
    import HelloWorld
    HelloWorld.say_hello()
    out, err = capsys.readouterr()
    assert(out == "Hello World!\n")
