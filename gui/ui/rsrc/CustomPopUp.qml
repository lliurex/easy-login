import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: popUpWaiting
    width: 570
    height: 100
    anchors.centerIn: Overlay.overlay
    modal: true
    focus: true
    visible: mainStackBridge.showPopUp.show
    closePolicy: Popup.NoAutoClose

    background: Rectangle {
        color: palette.window
        border.color: palette.mid
        radius: 4
    }

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 10

        Image{
            id:spinnerImage
            source: "/usr/share/easy-login/gui/rsrc/loading.png"
            Layout.preferredWidth: 24
            Layout.preferredHeight: 24
            Layout.alignment: Qt.AlignHCenter
            fillMode: Image.PreserveAspectFit
            smooth:false
            antialiasing:false
                rotation:0
        }
            
        Timer{
            id:rotationTimer
            running:(spinnerImage!==null && popUpWaiting!==null) && spinnerImage.visible && popUpWaiting.visible
            repeat:true
            interval:100

            onTriggered:{
                spinnerImage.rotation=(spinnerImage.rotation+330)%360
            }
        }
        
        Text {
            id: popupText
            text: getTextMessage()
            font.pointSize: 10
            color: palette.windowText
            Layout.alignment: Qt.AlignHCenter
            horizontalAlignment: Text.AlignHCenter
        }
    }

    function getTextMessage() {
        let code = mainStackBridge.showPopUp.msgCode;
        
        switch (code) {
            case 20: 
                return i18nd("easy-login", "Changing status. Wait a moment...");
            case 21:
                return i18nd("easy-login", "Removing the user. Wait a moment...");
            case 22:
                return i18nd("easy-login", "Removing all users. Wait a moment...");
            case 23:
                return i18nd("easy-login", "Generating PDF list. Wait a moment...");
            case 24:
                return i18nd("easy-login", "Loading configuration. Wait a moment...");
            case 25:
                return i18nd("easy-login", "Loading user information. Wait a moment...");
            case 26:
                return i18nd("easy-login", "Checking data. Wait a moment...");
            case 27:
                return i18nd("easy-login", "Saving data. Wait a moment...");
            case 28:
                return i18nd("easy-login", "Generating new password. Wait a moment...");
            default:
                return ""
        }
    }
}
