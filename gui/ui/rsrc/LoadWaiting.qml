import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

Rectangle {
    id: loadRoot
    visible: true
    color: "transparent"
    
    ColumnLayout {
        id: mainLoaderLayout
        anchors.centerIn: parent
        width: parent.width * 0.9
        spacing: 15

        ColumnLayout {
            Layout.alignment: Qt.AlignHCenter
            visible: !mainStackBridge.showLoadErrorMessage.show
            spacing: 10

            AnimatedImage {
                id: loadingGif
                source: "/usr/share/easy-login/gui/rsrc/loading.gif"
                Layout.preferredWidth: 32
                Layout.preferredHeight: 32
                Layout.alignment: Qt.AlignHCenter
                fillMode: Image.PreserveAspectFit
            }

            Text {
                id: loadText
                text: i18nd("easy-login", "Loading. Wait a moment...")
                font.pointSize: 10
                color: palette.windowText
                Layout.alignment: Qt.AlignHCenter
            }
        }

        Kirigami.InlineMessage {
            id: errorLabel
            visible: mainStackBridge.showLoadErrorMessage.show
            text: getMsgText(mainStackBridge.showLoadErrorMessage.msgCode)
            type: Kirigami.MessageType.Error
            Layout.fillWidth: true

        }
    }

    function getMsgText(msgCode) {
        switch (msgCode) {
            case -1:
                return i18nd("easy-login", "Unable to load configuration");
            default:
                return "";
        }
    }
}
