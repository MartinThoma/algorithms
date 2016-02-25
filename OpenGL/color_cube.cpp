#include <stdio.h>
#include <stdlib.h>
#include <X11/X.h>
#include <X11/Xlib.h>
#include <GL/gl.h>
#include <GL/glx.h>
#include <GL/glu.h>
#include <vector>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>


Display                 *dpy;
Window                  root;
GLint                   att[] = { GLX_RGBA, GLX_DEPTH_SIZE, 24, GLX_DOUBLEBUFFER, None };
XVisualInfo             *vi;
Colormap                cmap;
XSetWindowAttributes    swa;
Window                  win;
GLXContext              glc;
XWindowAttributes       gwa;
XEvent                  xev;

void DrawAQuad() {
    glClearColor(0.001f, 0.001f, 0.001f, 1.0);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    glMatrixMode(GL_PROJECTION);
    glm::mat4 projection;
    projection = glm::perspective(
            glm::radians(60.0f),
            float(gwa.width) / float(gwa.height),
             0.05f,
            200.0f);
    glLoadMatrixf((const float *)&projection);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glm::vec3 cam_pos(2.0f, 2.f, 2.0f);
    glm::vec3 cam_center(0.f, 0.f, 0.0f);
    glm::vec3 up(0.f, 0.f, 1.0f);

    // Define the camera
    gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2],
              cam_center[0], cam_center[1], cam_center[2],
              up[0], up[1], up[2]);

    // Define the vertices
    std::vector<glm::vec3> vertices, colors;
    vertices.push_back(glm::vec3(-1, -1, -1));
    vertices.push_back(glm::vec3(-1, -1, 1));
    vertices.push_back(glm::vec3(-1, 1, 1));
    vertices.push_back(glm::vec3(-1, -1, -1));
    vertices.push_back(glm::vec3(-1, 1, 1));
    vertices.push_back(glm::vec3(-1, 1, -1));
    vertices.push_back(glm::vec3(-1, -1, -1));
    vertices.push_back(glm::vec3(1, -1, 1));
    vertices.push_back(glm::vec3(-1, -1, 1));
    vertices.push_back(glm::vec3(-1, -1, -1));
    vertices.push_back(glm::vec3(1, -1, -1));
    vertices.push_back(glm::vec3(1, -1, 1));
    vertices.push_back(glm::vec3(-1, -1, -1));
    vertices.push_back(glm::vec3(-1, 1, -1));
    vertices.push_back(glm::vec3(1, 1, -1));
    vertices.push_back(glm::vec3(-1, -1, -1));
    vertices.push_back(glm::vec3(1, 1, -1));
    vertices.push_back(glm::vec3(1, -1, -1));
    vertices.push_back(glm::vec3(1, 1, 1));
    vertices.push_back(glm::vec3(1, 1, -1));
    vertices.push_back(glm::vec3(-1, 1, -1));
    vertices.push_back(glm::vec3(1, 1, 1));
    vertices.push_back(glm::vec3(-1, 1, -1));
    vertices.push_back(glm::vec3(-1, 1, 1));
    vertices.push_back(glm::vec3(1, 1, 1));
    vertices.push_back(glm::vec3(-1, 1, 1));
    vertices.push_back(glm::vec3(-1, -1, 1));
    vertices.push_back(glm::vec3(1, 1, 1));
    vertices.push_back(glm::vec3(-1, -1, 1));
    vertices.push_back(glm::vec3(1, -1, 1));
    vertices.push_back(glm::vec3(1, 1, 1));
    vertices.push_back(glm::vec3(1, -1, 1));
    vertices.push_back(glm::vec3(1, -1, -1));
    vertices.push_back(glm::vec3(1, 1, 1));
    vertices.push_back(glm::vec3(1, -1, -1));
    vertices.push_back(glm::vec3(1, 1, -1));
    colors = vertices;  // The colors are equal to the vertices.
    glBegin(GL_TRIANGLES);
        for (unsigned int i = 0; i < vertices.size(); ++i)
        {
            glColor3fv(&colors[i][0]);
            glVertex3fv(&vertices[i][0]);
        }
    glEnd();
}


int main(int argc, char *argv[]) {

    dpy = XOpenDisplay(NULL);

    if(dpy == NULL) {
        printf("cannot connect to X server\n\n");
        return 0;
    }

    root = DefaultRootWindow(dpy);

    vi = glXChooseVisual(dpy, 0, att);

    if(vi == NULL) {
        printf("no appropriate visual found\n\n");
        return 0;
    } else {
        printf("visual %p selected\n", (void *)vi->visualid); /* %p creates hexadecimal output like in glxinfo */
    }


    cmap = XCreateColormap(dpy, root, vi->visual, AllocNone);

    swa.colormap = cmap;
    swa.event_mask = ExposureMask | KeyPressMask;

    win = XCreateWindow(dpy, root, 0, 0, 600, 600, 0, vi->depth, InputOutput, vi->visual, CWColormap | CWEventMask, &swa);

    XMapWindow(dpy, win);
    XStoreName(dpy, win, "OpenGL Color Cube Example");

    glc = glXCreateContext(dpy, vi, NULL, GL_TRUE);
    glXMakeCurrent(dpy, win, glc);

    glEnable(GL_DEPTH_TEST);

    // Define "Close Window"
    Atom WM_DELETE_WINDOW = XInternAtom(dpy, "WM_DELETE_WINDOW", False);
    XSetWMProtocols(dpy, win, &WM_DELETE_WINDOW, 1);

    while(1) {
        XNextEvent(dpy, &xev);

        if(xev.type == Expose) {
            XGetWindowAttributes(dpy, win, &gwa);
            glViewport(0, 0, gwa.width, gwa.height);
            DrawAQuad();
            glXSwapBuffers(dpy, win);
        } else if(xev.type == KeyPress || xev.type == ClientMessage) {
            glXMakeCurrent(dpy, None, NULL);
            glXDestroyContext(dpy, glc);
            XDestroyWindow(dpy, win);
            XCloseDisplay(dpy);
            break;
        }
    }

    return 0;
}
