#include <windows.h>
#include <DbgHelp.h>

LONG myCrashHandle(EXCEPTION_POINTERS *pException)
{
    char dumpFileName[] = "standard.dmp";
    HANDLE hDumpFile = CreateFile(
        dumpFileName,
        GENERIC_WRITE,
        0,
        NULL,
        CREATE_ALWAYS,
        FILE_ATTRIBUTE_NORMAL | FILE_FLAG_WRITE_THROUGH,
        NULL);

    if (hDumpFile != INVALID_HANDLE_VALUE)
    {
        MINIDUMP_EXCEPTION_INFORMATION dumpInfo;
        dumpInfo.ExceptionPointers = pException;
        dumpInfo.ThreadId = GetCurrentThreadId();
        dumpInfo.ClientPointers = TRUE;
        MiniDumpWriteDump(
            GetCurrentProcess(),
            GetCurrentProcessId(),
            hDumpFile,
            (MINIDUMP_TYPE)(MiniDumpWithDataSegs | MiniDumpWithProcessThreadData | MiniDumpWithUnloadedModules),
            &dumpInfo,
            NULL,
            NULL);
    }

    return EXCEPTION_EXECUTE_HANDLER;
}

void makeDump()
{
    __try
    {
        int * a;
        a = (int*)0x100;
        *a = 0;
        //SetUnhandledExceptionFilter((LPTOP_LEVEL_EXCEPTION_FILTER)myCrashHandle);
    }
    __except (myCrashHandle(GetExceptionInformation()))
    {
    }
}

int main()
{
    makeDump();

    return 0;
}