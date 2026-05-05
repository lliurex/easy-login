import org.kde.kirigami as Kirigami
import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Rectangle{
    color:"transparent"

    Text{ 
        text:{
            switch(userStackBridge.actionType){
                case "add":
                    i18nd("easy-login","New User")
                    break;
                case "edit":
                    i18nd("easy-login","Edit User")
                    break;
              }
        }
        font.pointSize: 16
    }
    
    GridLayout{
        id:generalLayout
        rows:3
        flow: GridLayout.TopToBottom
        rowSpacing:10
        width:parent.width-10
        anchors.horizontalCenter:parent.horizontalCenter
  
        Kirigami.InlineMessage {
            id: messageLabel
            visible:userStackBridge.showUserFormMessage[0]
            text:getMessageText()
            type:Kirigami.MessageType.Error
            Layout.minimumWidth:650
            Layout.fillWidth:true
            Layout.topMargin: 40
        }

        GridLayout{
            id:dataGrid
            columns:2
            flow: GridLayout.LeftToRight
            columnSpacing:5
            rowSpacing:15
            Layout.topMargin: messageLabel.visible?0:40
            Layout.alignment:Qt.AlignHCenter

            Text{
                id:nameText
                text:i18nd("easy-login","Name:")
                Layout.alignment:Qt.AlignRight
            }
            TextField{
                id:nameEntry
                text:userStackBridge.name
                horizontalAlignment:TextInput.AlignLeft
                implicitWidth:400
                onTextChanged:{
                    userStackBridge.updateNameValue(nameEntry.text)
                }
            }

            Text{
                id:surnameText
                text:i18nd("easy-login","Surname:")
                Layout.alignment:Qt.AlignRight
            }
            TextField{
                id:surnameEntry
                text:userStackBridge.surname
                horizontalAlignment:TextInput.AlignLeft
                implicitWidth:400
                onTextChanged:{
                    userStackBridge.updateSurnameValue(surnameEntry.text)
                }
            }

            Text{
                id:loginText
                text:i18nd("easy-login","Login:")
                Layout.alignment:Qt.AlignRight
            }
            RowLayout{
                Layout.alignment:Qt.AlignLeft
                spacing:10
                TextField{
                    id:loginEntry
                    text:userStackBridge.login
                    enabled: userStackBridge.enableLoginEdition
                    horizontalAlignment:TextInput.AlignLeft
                    implicitWidth:400
                    onTextChanged:{
                        userStackBridge.updateLoginValue(loginEntry.text)
                    }
                }
                Button {
                    id:editLoginBtn
                    display:AbstractButton.IconOnly
                    icon.name:"document-edit.svg"
                    Layout.preferredHeight: 35
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("easy-login","Click to edit login")
                    onClicked:userStackBridge.forceLoginEdition()
    
                }

            }
            Text{
                id:pwdText
                text:i18nd("easy-login","Password:")
                Layout.alignment:Qt.AlignRight
            }
            RowLayout{
                Layout.alignment:Qt.AlignLeft
                spacing:10

                Rectangle{
                    id:containerImg1
                    width:80
                    height:80
                    border.color: "#ffffff"
                    border.width:5
                    color:"transparent"

                    Image{
                        id:pwdImg1
                        width:60
                        height:60
                        anchors.centerIn:parent
                        fillMode:Image.PreserveAspectFit
                        source:userStackBridge.pwdImgPaths[0]
                    }
                }

                Rectangle{
                    id:containerImg12
                    width:80
                    height:80
                    border.color: "#ffffff"
                    border.width:5
                    color:"transparent"

                    Image{
                        id:pwdImg2
                        width:60
                        height:60
                        anchors.centerIn:parent
                        fillMode:Image.PreserveAspectFit
                        source:userStackBridge.pwdImgPaths[1]
                    }
                }

                Rectangle{
                    id:containerImg3
                    width:80
                    height:80
                    border.color: "#ffffff"
                    border.width:5
                    color:"transparent"

                    Image{
                        id:pwdImg3
                        width:60
                        height:60
                        anchors.centerIn:parent
                        fillMode:Image.PreserveAspectFit
                        source:userStackBridge.pwdImgPaths[2]
                    }
                }

                Rectangle{
                    id:containerImg4
                    width:80
                    height:80
                    border.color: "#ffffff"
                    border.width:5
                    color:"transparent"

                    Image{
                        id:pwdImg4
                        width:60
                        height:60
                        anchors.centerIn:parent
                        fillMode:Image.PreserveAspectFit
                        source:userStackBridge.pwdImgPaths[3]
                    }
                }

                Button {
                    id:refreshPwdBtn
                    display:AbstractButton.IconOnly
                    icon.name:"document-edit.svg"
                    Layout.preferredHeight: 35
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("easy-login","Click to refresh password")
                    onClicked:userStackBridge.generateUsername()
    
                }
            }
        }
       
    }
    RowLayout{
        id:btnBox
        anchors.bottom: parent.bottom
        anchors.right:parent.right
        anchors.bottomMargin:15
        anchors.rightMargin:10
        spacing:10

        Button {
            id:applyBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-ok.svg"
            text:i18nd("easy-login","Apply")
            Layout.preferredHeight:40
            enabled:userStackBridge.changesInUser
            onClicked:{
                closeTimer.stop()
                userStackBridge.applyUserChanges()
                
            }
        }
        Button {
            id:cancelBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-cancel.svg"
            text:i18nd("easy-login","Cancel")
            Layout.preferredHeight: 40
            enabled:userStackBridge.changesInUser
            onClicked:{
               userStackBridge.cancelUserChanges()
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
                var msg=i18nd("easy-login","You must indicate a name for the user");
                break;
            case -5:
                var msg=i18nd("easy-login","You must indicate a surnanme for the user");
                break;
            case -6:
                var msg=i18nd("easy-login","You must indicate a login for the user");
                break;
            default:
                var msg=""
                break
        }
        return msg    

    }
   
}
