from distutils.core import setup, Extension


def main():
    extensions = [
        Extension(
            "key_tracker_x86",
            ["key_tracker_c/key_tracker.c"],
            extra_compile_args=["-m32"],
            extra_link_args=["-m32"],
        ),
        Extension(
            "key_tracker_x64",
            ["key_tracker_c/key_tracker.c"],
            extra_compile_args=["-m64"],
            extra_link_args=["-m64"],
        ),
    ]

    setup(
        name="key_tracker",
        version="1.0.0",
        description="Returns fast Keyboard-inputs on Windows and Linux",
        url="https://github.com/Muddyblack/Key_Tracker",
        author="Muddyblack",
        author_email="Muddyblack03@gmail.com",
        python_requires="==3.11.*",
        ext_modules=extensions,
    )


if __name__ == "__main__":
    main()
