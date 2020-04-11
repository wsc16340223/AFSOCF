#include "MyFileClass.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MyFileClass w;
    w.show();
    return a.exec();
}
