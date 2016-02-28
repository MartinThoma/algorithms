#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>

void display(void) {
    // clear all pixels
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    glBegin(GL_TRIANGLES);
        glVertex3f( 0.0f, 0.0f, 0.0f );
        glVertex3f( 1.0f, 0.0f, 0.0f );
        glVertex3f( 0.0f, 1.0f, 0.0f );
    glEnd();
    glutSwapBuffers();
}

void init (void) {
    // select clearing (background) color
    glClearColor(1.0f, 0.0f, 0.0f, 1.0f);
    glClearDepth(1.0f);

    glEnable(GL_LIGHTING);
    glEnable(GL_LIGHT0);
    glEnable(GL_DEPTH_TEST);
}

// Is called when the size of the window is changed.
// Changes projection matrices
void resize(int w, int h) {
    glMatrixMode( GL_MODELVIEW );
    glLoadIdentity();
    gluLookAt(0.0, 0.0, 5.0, // position
              0.0, 0.0, 0.0, // look there
              0.0, 1.0, 0.0 ); // Up vector
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(65.0, (float)w / h, 1.0, 100.0 );
    glViewport(0, 0, (unsigned int)w, (unsigned int)h);
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    // initialize and open window with rendering context
    int mode = GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH;
    glutInitDisplayMode(mode);
    glutInitWindowSize(1024, 768);
    glutCreateWindow("The title of your glut program");

    // initialize OpenGL states and program pipeline
    init();

    // register callback functions
    glutDisplayFunc ( display );
    glutReshapeFunc ( resize);
    /*glutKeyboardFunc( keyboard );
    glutMouseFunc( mouse);
    glutIdleFunc( idle);*/
    glutMainLoop();
    return 0;
}
