import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

Rectangle{
    visible: true
    color:"transparent"

    GridLayout{
        id: loadGrid
        rows: 3
        flow: GridLayout.TopToBottom
        anchors.centerIn:parent

        RowLayout{
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter
            visible:!mainStackBridge.showLoadErrorMessage[0]

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

        RowLayout{
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter
            visible:!mainStackBridge.showLoadErrorMessage[0]

            Text{
                id:loadtext
                text:i18nd("easy-login", "Loading. Wait a moment...")
                font.pointSize: 10
                Layout.alignment:Qt.AlignHCenter
            }
        }
        Kirigami.InlineMessage {
            id: errorLabel
            visible:mainStackBridge.showLoadErrorMessage[0]
            text:getMsgText(mainStackBridge.showLoadErrorMessage[1])
            type:Kirigami.MessageType.Error;
            Layout.minimumWidth:750
            Layout.fillWidth:true
            Layout.rightMargin:15
            Layout.leftMargin:15
        }
    }

    function getMsgText(msgCode){

        switch (msgCode){
            case -1:
                var msg=i18nd("easy-login","Enable to load configuration")
                break;
            default:
                var msg=""
                break;
        }
        return msg

    }
}
