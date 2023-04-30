#include <Python.h>

#ifdef _WIN32
// Windows specific includes
#include <conio.h>
#else
// Unix specific includes
#include <termios.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/types.h>
#endif

static PyObject *read_key(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ""))
    {
        return NULL;
    }

#ifdef _WIN32
    // Windows implementation
    int key = 0;
    if (_kbhit())
    {
        key = _getch();
    }
#else
    // Unix implementation
    struct termios old_tio, new_tio;
    tcgetattr(STDIN_FILENO, &old_tio);
    new_tio = old_tio;
    new_tio.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &new_tio);

    int key = 0;
    char buf = 0;
    ssize_t n;
    if ((n = read(STDIN_FILENO, &buf, 1)) > 0)
    {
        key = buf;
    }

    tcsetattr(STDIN_FILENO, TCSANOW, &old_tio);
#endif

    return Py_BuildValue("i", key);
}

static PyMethodDef keyboardMethods[] = {
    {"read_key", read_key, METH_VARARGS, "Reads a single key from the keyboard."},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef keyboardModule = {
    PyModuleDef_HEAD_INIT,
    "custom_keyboard",
    NULL,
    -1,
    keyboardMethods};

PyMODINIT_FUNC PyInit_key_tracker_x86_64(void)
{
    return PyModule_Create(&keyboardModule);
}
