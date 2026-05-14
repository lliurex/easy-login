import org.kde.kirigami as Kirigami
import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import QtQml

Rectangle {
    id: rectLayout
    color: "transparent"

    Text {
        id: titleText
        text: i18nd("easy-login", "Configuration")
        font.pointSize: 16
        anchors.top: parent.top
        anchors.left: parent.left
    }

    ColumnLayout {
        id: mainContent
        anchors.top: titleText.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: btnBox.top
        anchors.leftMargin: 5
        anchors.rightMargin:15
        anchors.topMargin:10
        anchors.bottomMargin:25
        spacing: 10

        Kirigami.InlineMessage {
            id: messageLabel
            Layout.fillWidth: true
            visible: usersOptionsStackBridge.showMainMessage.show
            text: getTextMessage(usersOptionsStackBridge.showMainMessage.msgCode)
            type: getTypeMessage(usersOptionsStackBridge.showMainMessage.type)
        }

        RowLayout {
            id: enableLoginbox
            Layout.fillWidth: true
            
            Text {
                text: i18nd("easy-login", "Activate Easy-Login:")
                font.pointSize: 10
                Layout.alignment: Qt.AlignVCenter
            }

            Switch {
                id: enableSwitch
                checked: usersOptionsStackBridge.easyLoginEnabled
                Layout.alignment: Qt.AlignVCenter
                onToggled: {
                    usersOptionsStackBridge.enableEasyLogin(checked)
                }
            }
        }

        UsersList {
            id: usersList
            usersModel: usersOptionsStackBridge.usersModel
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    RowLayout {
        id: btnBox
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin:5
        anchors.margins:15
        height: 50
        spacing: 10

        Button {
            id: globalActionsBtn
            display: AbstractButton.TextBesideIcon
            icon.name: "run-build"
            text: i18nd("easy-login", "Global Options")
            enabled: usersOptionsStackBridge.enableGlobalOptions
            onClicked: optionsMenu.open()
            
            Menu {
                id: optionsMenu
                y: -height - 5
                x: globalActionsBtn.width/2
                MenuItem {
                    icon.name: "document-print"
                    text: i18nd("easy-login", "Generate PDF list")
                    onClicked: pdfFileDialog.open()
                }
                MenuItem {
                    icon.name: "delete"
                    text: i18nd("easy-login", "Delete all users")
                    onClicked: usersOptionsStackBridge.removeUser([true])
                }
            }
        }

        Item {
            Layout.fillWidth: true
        }

        Button {
            id: newBtn
            display: AbstractButton.TextBesideIcon
            icon.name: "list-add"
            text: i18nd("easy-login", "New user")
            onClicked: userStackBridge.addNewUser() 
        }
    }

    ChangesDialog {
        id: removeUserDialog
        dialogIcon: "dialog-warning"
        dialogMsg: usersOptionsStackBridge.showRemoveUserDialog.allUsers 
                   ? i18nd("easy-login", "All users will be deleted.\nDo you want to continue?") 
                   : i18nd("easy-login", "The user will be deleted.\nDo you want to continue?")
        dialogVisible: usersOptionsStackBridge.showRemoveUserDialog.show
        dialogWidth: 400
        btnAcceptVisible: false
        btnDiscardText: i18nd("easy-login", "Accept")
        btnDiscardIcon: "dialog-ok"
        btnDiscardVisible: true
        btnCancelText: i18nd("easy-login", "Cancel")
        btnCancelIcon: "dialog-cancel"
        
        Connections {
           target: removeUserDialog
           function onDiscardDialogClicked() { usersOptionsStackBridge.manageRemoveUserDialog('Accept') }
           function onRejectDialogClicked() { usersOptionsStackBridge.manageRemoveUserDialog('Cancel') }
        }
    }

    FileDialog {
        id: pdfFileDialog
        title: i18nd("easy-login", "Please choose a file to save pdf list")
        fileMode: FileDialog.SaveFile       
        currentFolder: StandardPaths.standardLocations(StandardPaths.HomeLocation)[0]
        nameFilters: ["PDF files (*.pdf)"]
        onAccepted: {
            let path = selectedFile.toString().replace("file://", "")
            usersOptionsStackBridge.generateList(path)
        }
    }

    function getTextMessage(msgCode) {
        switch (msgCode) {
            case -2:
                return i18nd("easy-login", "Unable to add user")
            case -3:
                return i18nd("easy-login", "Unable to save the changes")
            case -7:
                return i18nd("easy-login", "Unable to remove user")
            case -8:
                return i18nd("easy-login", "Unable to remove all users")
            case -10:
                return i18nd("easy-login", "Unable to generate PDF list")
            case -11:
                return i18nd("easy-login", "Unable to load user info")
            case 0:
                return i18nd("easy-login", "Changes saved successfully")
            case 2:
                return i18nd("easy-login", "User removed successfully")
            case 3:
                return i18nd("easy-login", "The state change has been performed successfully")
            case 4:
                return i18nd("easy-login", "Users removed successfully")
            case 5:
                return i18nd("easy-login", "PDF list generated successfully")
            default:
                return ""
        }
    }

    function getTypeMessage(msgType) {
        switch (msgType) {
            case "Information":
                return Kirigami.MessageType.Information
            case "Ok":
                return Kirigami.MessageType.Positive
            case "Error":
                return Kirigami.MessageType.Error
            case "Warning":
                return Kirigami.MessageType.Warning
            default:
                return Kirigami.MessageType.Information
        }
    }
}
