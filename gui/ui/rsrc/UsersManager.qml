import org.kde.kirigami as Kirigami
import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

Rectangle{
    id:rectLayout
    color:"transparent"
    Text{ 
        text:i18nd("easy-login","Configuration")
        font.pointSize: 16
    }

    property var backupAction:undefined

    GridLayout{
        id:generalUsersLayout
        rows:3
        flow: GridLayout.TopToBottom
        rowSpacing:10
        anchors.left:parent.left
        width:parent.width-10
        height:parent.height-120
        enabled:true
        Kirigami.InlineMessage {
            id: messageLabel
            visible:usersOptionsStackBridge.showMainMessage[0]
            text:getTextMessage(usersOptionsStackBridge.showMainMessage[1])
            type:getTypeMessage(usersOptionsStackBridge.showMainMessage[2])
            Layout.minimumWidth:650
            Layout.fillWidth:true
            Layout.topMargin: 40
        }

        RowLayout {
            id:enableLoginbox
            Layout.topMargin: messageLabel.visible?0:40
            Text {
                id:enableLoginText
                text:i18nd("easy-login","Activate Easy-Login:")
                font.pointSize: 10
                Layout.alignment:Qt.AlignVCenter
                Layout.leftMargin:5
            }

            Switch {
                id:enableSwitch
                checked: usersOptionsStackBridge.easyLoginEnabled
                Layout.alignment:Qt.AlignVCenter|Qt.AlignHLeft
                Layout.rightMargin:5
                indicator: Rectangle {
                    implicitWidth: 40
                    implicitHeight: 10
                    x: enableSwitch.width - width - enableSwitch.rightPadding
                    y: parent.height/2 - height/2 
                    radius: 7
                    color: enableSwitch.checked ? "#3daee9" : "#d3d3d3"
                    Rectangle {
                        x: enableSwitch.checked ? parent.width - width : 0
                        width: 20
                        height: 20
                        y:parent.height/2-height/2
                        radius: 10
                        border.color: "#808080"
                    }
                }
                onToggled: {
                    usersOptionsStackBridge.enableEasyLogin(enableSwitch.checked)
                }
            }
        }
            
        UsersList{
            id:usersList
            usersModel:usersOptionsStackBridge.usersModel
            Layout.fillHeight:true
            Layout.fillWidth:true
            Layout.topMargin:0
        }
    }
    
    RowLayout{
        id:btnBox
        anchors.bottom: parent.bottom
        anchors.fill:parent.fill
        anchors.bottomMargin:15
        spacing:10

        Button {
            id:globalActionsBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"run-build.svg"
            text:i18nd("easy-login","Global Options")
            enabled:usersOptionsStackBridge.enableGlobalOptions
            Layout.preferredHeight:40
            Layout.rightMargin:rectLayout.width-(newBtn.width+150)
            onClicked:optionsMenu.open()
            
            Menu{
                id:optionsMenu
                y: -globalActionsBtn.height*1.7
                x: globalActionsBtn.width/2

                MenuItem{
                    icon.name:"delete.svg"
                    text:i18nd("easy-login","Delete all users")
                    onClicked:usersOptionsStackBridge.removeUser([true])
                }
       
            }
           
        }

        Button {
            id:newBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"list-add.svg"
            text:i18nd("easy-login","New user")
            Layout.preferredHeight:40
            onClicked:userStackBridge.addNewUser() 
        }
    }

    ChangesDialog{
        id:removeUserDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogMsg:{
            if (usersOptionsStackBridge.showRemoveUserDialog[1]){
                i18nd("easy-login","All users will be deleted.\nDo yo want to continue?")
            }else{
                i18nd("easy-login","The user will be deleted.\nDo yo want to continue?")
            }
        }
        dialogVisible:usersOptionsStackBridge.showRemoveUserDialog[0]
        dialogWidth:300
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardText:i18nd("easy-loging","Accept")
        btnDiscardIcon:"dialog-ok.svg"
        btnDiscardVisible:true
        btnCancelText:i18nd("easy-login","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
           target:removeUserDialog
           function onDiscardDialogClicked(){
                usersOptionsStackBridge.manageRemoveUserDialog('Accept')         
           }
           function onRejectDialogClicked(){
                usersOptionsStackBridge.manageRemoveUserDialog('Cancel')       
           }

        }
    }

    function getTextMessage(msgCode){
        switch (msgCode){
            case -2:
                var msg=i18nd("easy-logn","Unable to add user")
                break
            case -10:
                var msg=i18nd("easy-login","The state change has failed")
                break;
            case 0:
                var msg=i18nd("easy-login","User added successfully")
                break;
            case 11:
                var msg=i18nd("easy-login","The state change has been performed successfully")
                break;
            default:
                var msg=""
                break
        }
        return msg
    } 

    function getTypeMessage(msgType){

        switch (msgType){
            case "Information":
                return Kirigami.MessageType.Information
            case "Ok":
                return Kirigami.MessageType.Positive
            case "Error":
                return Kirigami.MessageType.Error
            case "Warning":
                return Kirigami.MessageType.Warning
        }
    }

} 
