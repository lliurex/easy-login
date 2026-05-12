import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

Item {
    id: root

    Timer{
        id:debounceTimer
        interval:500
        repeat:false
        property var callback
        onTriggered: if (callback) callback()

    }

    ColumnLayout {
        anchors.fill: parent
        anchors.rightMargin:15
        anchors.bottomMargin:25
        spacing:10
        
        Text{ 
            text: userStackBridge.actionType == "add"
                ?i18nd("easy-login", "New User")
                :i18nd("easy-login", "Edit User")
            font.pointSize: 16
        }

        Kirigami.InlineMessage {
            id: messageLabel
            visible: userStackBridge.showUserFormMessage[0]
            text: getMessageText()
            type: Kirigami.MessageType.Error
            Layout.fillWidth: true
        }

        GridLayout {
            columns: 2
            rowSpacing: 15
            columnSpacing: 5
            Layout.alignment: Qt.AlignHCenter
            Layout.topMargin: messageLabel.visible?0:30

            Text {
                text: i18nd("easy-login", "Name:")
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
            }
            TextField {
                id: nameEntry
                focus: true
                text: userStackBridge.name
                Layout.preferredWidth: 400
                onTextChanged: {
                    if (activeFocus){
                        debounceTimer.callback= ()=>userStackBridge.updateNameValue(text)
                        debounceTimer.restart()
                    }
                }
            }

            Text {
                text: i18nd("easy-login", "Surname:")
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
            }
            TextField {
                id: surnameEntry
                text: userStackBridge.surname
                Layout.preferredWidth: 400
                onTextChanged: {
                    if (activeFocus){
                        debounceTimer.callback= ()=>userStackBridge.updateSurnameValue(text)
                        debounceTimer.restart()
                    }
                }

            }

            Text {
                text: i18nd("easy-login", "Login:")
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
            }
            
            RowLayout {
                spacing: 10
                TextField {
                    id: loginEntry
                    text: userStackBridge.login
                    readOnly: !userStackBridge.enableLoginEdition
                    Layout.preferredWidth: 320
                    onTextChanged: {
                        debounceTimer.callback= ()=>userStackBridge.updateLoginValue(text)
                        debounceTimer.restart()
                    }   
                }
                Button {
                    icon.name: "document-edit"
                    enabled: !userStackBridge.enableLoginEdition
                    onClicked: userStackBridge.forceLoginEdition()
                    ToolTip.text: i18nd("easy-login", "Click to edit login")
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                }
                Button {
                    icon.name: "edit-reset"
                    enabled: userStackBridge.enableLoginEdition
                    onClicked: userStackBridge.restoreDefaultLogin()
                    ToolTip.text: i18nd("easy-login", "Click to restore login")
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                }
            }

            Text {
                text: i18nd("easy-login", "Password:")
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
            }
            RowLayout {
                spacing: 10
                Repeater {
                    model: 4
                    delegate: Rectangle {
                        width: 80; height: 80
                        border.color: "#ffffff"
                        border.width: 5
                        color: "transparent"
                        Image {
                            anchors.centerIn: parent
                            width: 60; height: 60
                            sourceSize.width: 120
                            sourceSize.height: 120
                            mipmap: true
                            smooth: true
                            source: userStackBridge.pwdImgPaths[index] || ""
                            fillMode: Image.PreserveAspectFit
                        }
                    }
                }
                Button {
                    icon.name: "view-refresh"
                    onClicked: userStackBridge.generateUsername()
                    ToolTip.text: i18nd("easy-login", "Click to get a new password")
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                }
            }
        }

        Item { Layout.fillHeight: true }

        RowLayout {
            Layout.alignment: Qt.AlignRight
            spacing: 10

            Button {
                text: i18nd("easy-login", "Apply")
                icon.name: "dialog-ok"
                enabled: userStackBridge.changesInUser
                onClicked: {
                    closeTimer.stop()
                    userStackBridge.applyUserChanges()
                }
            }
            Button {
                text: i18nd("easy-login", "Cancel")
                icon.name: "dialog-cancel"
                onClicked: {
                    closeTimer.stop()
                    userStackBridge.cancelUserChanges()
                }
            }
        }
    }

    ChangesDialog{
        id:settingsChangesDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogVisible:userStackBridge.showChangesInUserDialog
        dialogMsg:i18nd("easy-login","The are pending changes to save.\nDo you want save the changes or discard them?")
        dialogWidth:400
        btnAcceptVisible:true
        btnAcceptText:i18nd("easy-login","Apply")
        btnDiscardText:i18nd("easy-login","Discard")
        btnDiscardIcon:"delete.svg"
        btnDiscardVisible:true
        btnCancelText:i18nd("easy-login","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
            target:settingsChangesDialog
            function onDialogApplyClicked(){
                userStackBridge.manageChangesDialog("Accept")
            }
            function onDiscardDialogClicked(){
                userStackBridge.manageChangesDialog("Discard")           
            }
            function onRejectDialogClicked(){
                closeTimer.stop()
                userStackBridge.manageChangesDialog("Cancel")       
            }

        }
   }

   function getMessageText(){

         switch (userStackBridge.showUserFormMessage[1]){
            case -4:
                return i18nd("easy-login","You must indicate a name for the user");
            case -5:
                return i18nd("easy-login","You must indicate a surnanme for the user");
            case -6:
                return i18nd("easy-login","You must indicate a login for the user");
            default:
                return ""
        }

    }
}
