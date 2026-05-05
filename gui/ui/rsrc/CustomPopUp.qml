import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Popup {
    id:popUpWaiting
    width:570
    height:80
    anchors.centerIn: Overlay.overlay
    modal:true
    focus:true
    visible:!mainStackBridge.closePopUp[0]
    closePolicy:Popup.NoAutoClose

    GridLayout{
        id: popupGrid
        rows: 2
        flow: GridLayout.TopToBottom
        anchors.centerIn:parent


        RowLayout {
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter
            Rectangle{
                color:"transparent"
                width:30
                height:30
                AnimatedImage{
                    source: "/usr/share/easy-login/gui/rsrc/loading.gif"
                    transform: Scale {xScale:0.45;yScale:0.45}
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter

            Text{
                id:popupText
                text:getTextMessage()
                font.pointSize: 10
                Layout.alignment:Qt.AlignHCenter
            }
        }
    }

    function getTextMessage(){
        switch (mainStackBridge.closePopUp[1]){
            case 1:
                var msg=i18nd("easy-login","Loading configuration. Wait a moment...");
                break;
            case 2:
                var msg=i18nd("easy-login","Loading user info. Wait a moment...");
                break;
            case 22:
                var msg=i18nd("easy-login","Validating the data . Wait a moment...")
                break;
            case 23:
                var msg=i18nd("easy-login","Saving the data. Wait a moment...")
                break;
            case 10:
                var msg=i18nd("easy-login","Changing status. Wait a moment...")
                break;
            case 11:
                var msg=i18nd("easy-login","Removing the user. Wait a moment...")
                break;
            case 12:
                var msg=i18nd("easy-login","Removing all users. Wait a moment...")
                break;
            default:
                var msg=""
                break;
        }
        return msg
    }
}
