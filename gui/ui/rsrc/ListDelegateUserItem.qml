import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ItemDelegate {
    id: listUserItem
    
    property string username
    property string login
    property string name
    property string surname
    property string pwdImg1
    property string pwdImg2
    property string pwdImg3
    property string pwdImg4
    property string metaInfo

    enabled: true
    height: 70
    width: parent ? parent.width : 0

    background: Rectangle {
        color: "transparent"
    }

    contentItem: Item {
        id: containerItem

        MouseArea {
            id: mouseAreaOption
            anchors.fill: parent
            hoverEnabled: true
            propagateComposedEvents: true
            onEntered: {
                if (!optionsMenu.activeFocus) {
                    usersView.currentIndex = filterModel.visibleElements.indexOf(index)
                }
            }
        }

        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 15
            anchors.rightMargin: 15
            spacing: 20

            Text {
                id: loginText
                text: listUserItem.login
                font.pointSize: 10
                elide: Text.ElideMiddle
                Layout.fillWidth: true
                Layout.preferredWidth: 200
                verticalAlignment: Text.AlignVCenter
            }

            ColumnLayout {
                id: userInfo
                spacing: 2
                Layout.fillWidth: true
                Layout.preferredWidth: 200
                Layout.alignment: Qt.AlignVCenter

                Text {
                    text: listUserItem.name
                    font.pointSize: 10
                    elide: Text.ElideMiddle
                    Layout.fillWidth: true
                }
                Text {
                    text: listUserItem.surname
                    font.pointSize: 10
                    elide: Text.ElideMiddle
                    Layout.fillWidth: true
                }
            }

            Row {
                id: imagesRow
                spacing: 5
                Layout.alignment: Qt.AlignVCenter

                Image { source: pwdImg1; sourceSize: "24x24" }
                Image { source: pwdImg2; sourceSize: "24x24" }
                Image { source: pwdImg3; sourceSize: "24x24" }
                Image { source: pwdImg4; sourceSize: "24x24" }
            }

            Button {
                id: manageUserBtn
                display: AbstractButton.IconOnly
                icon.name: "configure.svg"
                visible: listUserItem.ListView.isCurrentItem
                
                Layout.alignment: Qt.AlignVCenter
                Layout.preferredWidth: visible ? implicitWidth : 0
                
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text: i18nd("easy-login","Click to manage this user")
                
                onClicked: optionsMenu.open()
                onVisibleChanged: if(!visible) optionsMenu.close()

                Menu {
                    id: optionsMenu
                    y: manageUserBtn.height
                    x: -(width - manageUserBtn.width / 2)

                    MenuItem {
                        text: i18nd("easy-login","Edit user")
                        icon.name: "document-edit.svg"
                        onClicked: userStackBridge.loadUser(username)
                    }
                    MenuItem {
                        text: i18nd("easy-login","Delete this user")
                        icon.name: "delete.svg"
                        onClicked: usersOptionsStackBridge.removeUser([false, username])
                    }
                }
            }
        }
    }
}
