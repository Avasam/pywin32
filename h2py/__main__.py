import os
import re
import subprocess
import sys
import tempfile

H2PY_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
ROOT_DIRECTORY = os.path.dirname(H2PY_DIRECTORY)
SDK_DIRECTORY = "C:/Program Files (x86)/Windows Kits/10/Include/10.0.22621.0"
MFC_DIRECTORY = "C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.38.33130/atlmfc"
INCLUDE = f"{SDK_DIRECTORY}/um;"
# INCLUDE += f"{SDK_DIRECTORY}/shared;"  # Explicitely don't include shared


def h2py_output_name(file_path: str):
    filename = os.path.split(file_path)[-1]
    # h2py will output to the current location, in all uppercase
    return os.path.splitext(filename)[0].upper() + ".py"


def run_h2py(header_file: str, include: bool):
    subprocess.run(
        [sys.executable, f"{H2PY_DIRECTORY}/h2py.py", header_file],
        env=dict(os.environ, INCLUDE=INCLUDE) if include else None,
    )
    return h2py_output_name(header_file)


def post_generation_fixes(file_content: str):
    print("Applying post-generation fixes...")
    # Add missing imports
    if "SNDMSG" in file_content:
        file_content = "from win32gui import SendMessage as SNDMSG\n\n" + file_content
    if "sizeof" in file_content:
        file_content = "from ctypes import sizeof\n\n" + file_content
    if "WM_USER" in file_content:
        # https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-user
        file_content = "WM_USER = 0x0400\n\n" + file_content
    # Special case to generate all SBPS_* constants for afxres
    if " = SBT_" in file_content:
        # https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-user
        file_content = (
            "from commctrl import SBT_NOBORDERS, SBT_OWNERDRAW, SBT_POPOUT\n\n"
            + file_content
        )
    # Update casts
    file_content = re.sub(r"(ASSERT)", "bool", file_content)
    # Uncomment returns
    file_content = re.sub(r"return +?#?#", "return ", file_content)
    # Remove private constants
    # file_content = re.sub(r"^_.+?$", "", file_content)

    return file_content


def generate(header_files: list[str], destination: str, include=True):
    destination = ROOT_DIRECTORY + "/" + destination

    concatenated_content = ""
    for header_file in header_files:
        h2py_output = run_h2py(header_file, include)
        # Append the output to the destination
        with open(h2py_output, "r", encoding="utf-8") as h2py_output_file:
            concatenated_content += h2py_output_file.read() + "\n"
        # Cleanup the h2py output file
        os.remove(h2py_output)

    concatenated_content = post_generation_fixes(concatenated_content)

    with open(destination, "w+", encoding="utf-8") as destination_file:
        destination_file.write(concatenated_content)


def main():
    # h2py.py works on the current directory, let's move to a temp folder
    dirpath = tempfile.mkdtemp()
    os.chdir(dirpath)

    # generate(  # TODO: A mess with lots of duplicates
    #     [f"{SDK_DIRECTORY}/um/objbase.h"],
    #     "com/win32com/storagecon.py",
    # )
    # generate(  # FIXME: Missing enums generation
    #     [
    #         f"{SDK_DIRECTORY}/um/Iads.h",
    #         f"{SDK_DIRECTORY}/um/AdsErr.h",
    #         f"{SDK_DIRECTORY}/um/ObjSel.h",
    #     ],
    #     "com/win32comext/adsi/adsicon.py",
    # )
    # generate(  # TODO: Manual stuff
    #     [
    #         f"{SDK_DIRECTORY}/um/PropIdl.h",
    #     ],
    #     "com/win32comext/ifilter/ifiltercon.py",
    #     include=False,
    # )
    # generate(  # Complete, BUT TODO: This makes some negative numbers positive, is that right??
    #     [f"{SDK_DIRECTORY}/um/urlmon.h"],
    #     "com/win32comext/internet/inetcon.py",
    # )
    # generate( # TODO: similar issues as mmsystem
    #     [
    #         f"{SDK_DIRECTORY}/um/ShlObj.h",
    # #         f"{SDK_DIRECTORY}/um/oleidl.h",
    # #         f"{SDK_DIRECTORY}/um/shellapi.h",
    #     ],
    #     "com/win32comext/shell/shellcon.py",
    #     include=False,  # ShlObj.h would cuase WAY TOO MUCH side inclusions, including a repeat of commctrl
    # )
    # generate( # Vendored + Unknown location
    #     ["Include/scintilla.h", "Include/scilexer.h"],
    #     "Pythonwin/pywin/scintilla/scintillacon.py",
    # )
    # generate(  # Complete. 3 missing variables are currently found in win32netcon
    #     [
    #         f"{SDK_DIRECTORY}/shared/wnnc.h",
    #         f"{SDK_DIRECTORY}/um/winnetwk.h",
    #     ],
    #     "win32/Demos/win32wnet/winnetwk.py",
    # )
    # generate(  # Complete
    #     [
    #         f"{MFC_DIRECTORY}/include/afxres.h",
    #         f"{MFC_DIRECTORY}/include/afxext.h",
    #     ],
    #     "win32/Lib/afxres.py",
    #     include=False,  # afxext.h would cuase WAY TOO MUCH side inclusions, we just want the SBPS_* constants
    # )
    # generate(  # FIXME: Still has some issues with certain definition order (like w/ SB_GETTIPTEXT and SB_SETTIPTEXT)
    #     [f"{SDK_DIRECTORY}/um/CommCtrl.h"],
    #     "win32/Lib/commctrl.py",
    # )
    # TODO: Generates a ton more than already exists, also definition order issue leading to unbound variables
    # If I could figure out how to generate the variabel MIXERCONTROL_CONTROLTYPE_BOOLEAN I might have my answer
    # generate(
    #     [
    #         f"{SDK_DIRECTORY}/um/mmsystem.h",
    #         # f"{SDK_DIRECTORY}/um/ime_cmodes.h",
    #         # f"{SDK_DIRECTORY}/um/mciapi.h",
    #         # f"{SDK_DIRECTORY}/um/mmiscapi.h",
    #     ],
    #     "win32/Lib/mmsystem.py",
    # )
    # generate(  # Complete
    #     [f"{SDK_DIRECTORY}/um/nb30.h"],
    #     "win32/Lib/netbioscon.py",
    # )
    # generate(
    #     [
    #         f"{SDK_DIRECTORY}/um/NtDsAPI.h",
    #         f"{SDK_DIRECTORY}/um/DsGetDC.h",
    #     ],
    #     "win32/Lib/ntsecuritycon.py",
    # )
    # generate(  # FIXME: Still missing a lot idk where they should come from
    #     [
    #         f"{SDK_DIRECTORY}/shared/sspi.h",
    #         f"{SDK_DIRECTORY}/um/minschannel.h",
    #     ],
    #     "win32/Lib/sspicon.py",
    # )
    # generate(
    #     [
    #         f"{SDK_DIRECTORY}/um/commdlg.h",
    #         f"{SDK_DIRECTORY}/um/winreg.h",
    #         f"{SDK_DIRECTORY}/um/WinUser.h",
    #         f"{SDK_DIRECTORY}/um/winnt.h",
    #         f"{SDK_DIRECTORY}/um/wingdi.h",
    #         f"{SDK_DIRECTORY}/um/Richedit.h",
    #         f"{SDK_DIRECTORY}/um/Dbt.h",
    #     ],
    #     "win32/Lib/win32con.py",
    # )
    # generate(  # Complete
    #     [f"{SDK_DIRECTORY}/um/wincrypt.h"],
    #     "win32/Lib/win32cryptcon.py",
    # )
    # generate(  # FIXME: unusable c methods
    #     [
    #         f"{SDK_DIRECTORY}/um/wininet.h",
    #         f"{SDK_DIRECTORY}/um/winhttp.h",
    #     ],
    #     "win32/Lib/win32inetcon.py",
    # )
    # generate(  # FIXME: Manual stuff
    #     [
    #         f"{SDK_DIRECTORY}/um/LMaccess.h",
    #         f"{SDK_DIRECTORY}/um/LMShare.h",
    #         f"{SDK_DIRECTORY}/um/winnetwk.h",
    #     ],
    #     "win32/Lib/win32netcon.py",
    # )
    # generate(  # FIXME: Lots of manual additions
    #     [f"{SDK_DIRECTORY}/shared/winerror.h"],
    #     "win32/Lib/winerror.py",
    # )
    # generate(  # FIXME: unusable c methods
    #     [f"{SDK_DIRECTORY}/um/winnt.h"],
    #     "win32/Lib/winnt.py",
    # )
    # generate(  # Complete
    #     [f"{SDK_DIRECTORY}/um/winperf.h"],
    #     "win32/Lib/winperf.py",
    # )

    # Format files after we're done generating
    subprocess.run(
        [
            sys.executable,
            "-m",
            "black",
            f"{ROOT_DIRECTORY}/win32/Lib",
            f"{ROOT_DIRECTORY}/win32/Demos/win32wnet/winnetwk.py",
            f"{ROOT_DIRECTORY}/com/win32comext",
            f"{ROOT_DIRECTORY}/com/win32com/storagecon.py",
        ]
    )


main()
