import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
import org.kde.kirigami as Kirigami

ApplicationWindow {
    id: mainWindow
    property bool closing: false
    property int margin: 1

    visible: true
    title: "Easy-Login"

    width: mainLayout.implicitWidth + 2 * margin
    height: mainLayout.implicitHeight + 2 * margin
    minimumWidth: mainLayout.Layout.minimumWidth + 2 * margin
    minimumHeight: mainLayout.Layout.minimumHeight + 2 * margin
    Component.onCompleted: {
        x = Screen.width / 2  - minimumWidth/2
        y = Screen.height / 2 - minimumHeight/2
    }

    onClosing: (close) => {
        close.accepted = closing;
        if (!closing) {
            mainStackBridge.closeEasyLogin();
            closeTimer.start();
        }
    }

    Timer {
        id: closeTimer
        interval: 100
        repeat: true
        onTriggered: {
            if (mainStackBridge.closeGui) {
                stop();
                mainWindow.closing = true;
                mainWindow.close();
            }
        }
    }

    ColumnLayout {
        id: mainLayout
        anchors.fill: parent
        Layout.minimumWidth:800
        Layout.minimumHeight:625

        Rectangle {
            id: bannerBox
            color: "#000000"
            Layout.fillWidth: true
            Layout.preferredHeight: 120

            Image {
                id: banner
                source: "/usr/share/easy-login/gui/rsrc/easy-login_banner.png"
                asynchronous: false
                anchors.centerIn: parent
                fillMode: Image.PreserveAspectFit
            }
        }

        StackView {
            id: mainView
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumHeight:500

            property int currentIndex: mainStackBridge.currentStack

            initialItem: loadView

            onCurrentIndexChanged: {
                switch (currentIndex) {
                    case 0: 
                        mainView.replace(loadView);
                        break;
                    case 1:
                        mainView.replace(listView);
                        break;
                    case 2:
                        mainView.replace(userView);
                        break;
                }
            }

            replaceEnter: Transition {
                NumberAnimation {
                    property: "opacity"
                    from: 0
                    to: 1
                    duration: 60
                }
            }
            replaceExit: Transition {
                NumberAnimation { 
                    property: "opacity"
                    from: 1
                    to: 0
                    duration: 60
                }
            }

            Component {
                id: loadView
                LoadWaiting {
                    id:loadWaiting
                }
            }
            Component {
                id: listView
                MainOptions {
                    id:mainOptions
                }
            }
            Component {
                id: userView
                UserOptions {
                    id:userOptions
                }
            }
        }
    }

    CustomPopUp {
        id: waitingPopUp
    }
}
