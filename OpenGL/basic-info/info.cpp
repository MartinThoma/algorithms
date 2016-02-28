#include <stdio.h>
#include <GL/gl.h>

int main(int argc, char *argv[]) {
    printf("GL_VENDOR: %s\n", glGetString(GL_VENDOR));
    printf("GL_RENDERER: %s\n", glGetString(GL_RENDERER));
    printf("GL_VERSION: %s\n", glGetString(GL_VERSION));
    printf("GL_EXTENSIONS: %s\n", glGetString(GL_EXTENSIONS));

    return 0;
}
