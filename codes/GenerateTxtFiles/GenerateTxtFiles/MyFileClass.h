#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_MyFileClass.h"

class MyFileClass : public QMainWindow
{
    Q_OBJECT

public:
    MyFileClass(QWidget *parent = Q_NULLPTR);
private slots:
    void on_pushButton_clicked();
private:
    void generateTextFiles();

    Ui::MyFileClassClass ui;
};
