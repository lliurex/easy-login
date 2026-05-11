import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    id: mainGrid
    spacing: 10
    Layout.fillWidth: true
    Layout.fillHeight: true

    Rectangle {
        id: sideBar
        width: 120
        Layout.fillHeight: true
        border.color: palette.mid

        ColumnLayout {
            id: menuLayout
            Layout.fillWidth: true
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
        }
    }

    StackView {
        id: optionsView
        Layout.fillWidth: true
        Layout.fillHeight: true

        property int currentIndex: mainStackBridge.mainCurrentOption
        initialItem: usersView

        onCurrentIndexChanged: {
            if (currentIndex === 0) {
                optionsView.replace(usersView)
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
