import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    id: mainGrid
    spacing: 10

    Rectangle {
        id: sideBar
        width: 125
        Layout.fillHeight: true
        border.color: palette.mid

        ColumnLayout {
            id: menuLayout
            anchors.fill:parent
            spacing: 0

            MenuOptionBtn {
                id: listItem
                Layout.fillWidth: true
                optionText: i18nd("easy-login", "Users")
                optionIcon: "group"
                onMenuOptionClicked: mainStackBridge.moveToMainOptions(0)
            }

            MenuOptionBtn {
                id: helpItem
                Layout.fillWidth: true
                optionText: i18nd("easy-login", "Help")
                optionIcon: "help-contents"
                onMenuOptionClicked: mainStackBridge.openHelp()
            }

            Item {
                    Layout.fillHeight:true

            }
        }
    }

    StackView {
        id: optionsView
        Layout.fillWidth: true
        Layout.fillHeight: true

        property int currentIndex: mainStackBridge.mainCurrentOption
        initialItem: usersView

        onCurrentIndexChanged: {
            switch(currentIndex){
                case 0:
                    optionsView.replace(usersView)
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
            id: usersView
            UsersManager {
                id: userManager
            }
        }
    }
}
