import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


RowLayout{
    id: usersGrid
    spacing: 10

    ColumnLayout{
        Layout.fillHeight:true
        spacing: 5

        MenuOptionBtn {
            id:goBackBtn
            optionText:i18nd("easy-login","Users")
            optionIcon:"go-previous.svg"
            optionPointSize:14
            onMenuOptionClicked:userStackBridge.goHome()
        }  
        Rectangle{
            width: 125
            Layout.fillHeight: true
            border.color: palette.mid
            ColumnLayout{
                anchors.fill:parent
                spacing:0

                MenuOptionBtn {
                    id:infoItem
                    optionText:i18nd("easy-login","User")
                    optionIcon:"user.svg"
                }
                Item {
                    Layout.fillHeight:true

                }

            }
        }
    }

    StackView {
        id: manageView
        property int currentOption:userStackBridge.userCurrentOption
        Layout.fillWidth:true
        Layout.fillHeight: true
        initialItem:emptyView

        onCurrentOptionChanged:{
            switch(currentOption){
                case 0:
                    manageView.replace(emptyView)
                    break;
                case 1:
                    manageView.replace(userView)
                    break;
            }

        }
        replaceEnter: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 0
                to:1
                duration: 60
            }
        }
        replaceExit: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 1
                to:0
                duration: 60
            }
        }

        Component{
            id:emptyView
            Item{
                id:emptyPanel
            }
        }
        
        Component{
            id:userView
            UserForm{
                id:userForm
            }
        }
        
    }
}

