#include "MyFileClass.h"

#include <string>
#include <vector>
#include <fstream>
#include <ctime>
#include <windows.h>

#include <QString>
#include <QDateTime>
#include <QMessageBox>

using namespace std;

MyFileClass::MyFileClass(QWidget *parent)
    : QMainWindow(parent)
{
    ui.setupUi(this);
}

void MyFileClass::generateTextFiles()
{
    vector<string> SoftwareVersion = { "CAD Version1", "CAD Version2", "CAD Version3", "CAD Version4" };
    vector<string> ErrorType = {
        "length_error", "domain_error", "out_of_range", "invalid_argument",
        "range_error", "overflow_error", "underflow_error", "bad_alloc",
        "bad_exception", "bad_typeid", "bad_cast", "ios_base::failure"
    };
    vector<string> OSInfo = { "Microsoft Windows 7 32-bit", "Microsoft Windows 7 64-bit",
        "Microsoft Windows 10 32-bit", "Microsoft Windows 10 64-bit" };
    vector<string> OpenGLInfo = { "3.3.0", "4.3.0", "4.6.0" };
    vector<string> myMonth = { "01", "02", "03","04","05","06","07","08","09","10","11","12" };
    vector<string> myYear = { "2017", "2018", "2019", "2020" };

    QString currentTime;
    QString qFileName;
    string fileName;
    ofstream txtFile;

    for (int i = 0; i < 1000; i++)
    {
        srand((int)time(0));

        //currentTime = QDateTime::currentDateTime().toString("MMddyyyy_HHmmss_zzz");
        currentTime = QDateTime::currentDateTime().toString("_HHmmss_zzz");
        int mDay = rand() % 31 + 1;
        QString qDay;
        if (mDay < 10)
        { qDay = "0" + QString::number(mDay); }
        else
        { qDay = QString::number(mDay); }
        currentTime = QString::fromStdString(myMonth[rand() % myMonth.size()]) + qDay + QString::fromStdString(myYear[rand() % myYear.size()]) + currentTime;

        qFileName = "D:\\CrashReport\\receiveFiles\\" + currentTime + "_CrashReport.txt";
        fileName = qFileName.toStdString();
        txtFile.open(fileName);

        txtFile << "Software Version:" << endl << SoftwareVersion[rand() % SoftwareVersion.size()] << endl << endl
            << "Error Type:" << endl << ErrorType[rand() % ErrorType.size()] << endl << endl
            << "Occur Time:" << endl << currentTime.toStdString() << endl << endl
            << "User:" << endl << "user" << rand() % 50 << endl << endl
            << "OS Information:" << endl << OSInfo[rand() % OSInfo.size()] << endl << endl
            << "OpenGL Version:" << endl << OpenGLInfo[rand() % OpenGLInfo.size()] << endl << endl;
        txtFile.close();
        Sleep(1000);
    }
}

void MyFileClass::on_pushButton_clicked()
{
    generateTextFiles();

    QMessageBox::information(this, "Generate Files", "Generate finished", QMessageBox::Ok, QMessageBox::Ok);
}