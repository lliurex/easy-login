import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami


ItemDelegate {
    id: listUserItem
    
    property string username
    property string login
    property string name
    property string surname
    property list<string> pwdImgPaths
    property string metaInfo

    enabled: true
    height: 60
    width: parent ? parent.width-10 : 0
    hoverEnabled:true

    leftPadding:15
    rightPadding:15

    background:Rectangle {
        x:5
        y:5
        width:parent.width-10
        height:parent.height-5 
        color: (listUserItem.hovered || listUserItem.ListView.isCurrentItem)
                ?Qt.alpha(Kirigami.Theme.highlightColor,0.15)
                :"transparent"
        radius:6
        border.width:1
        border.color:(listUserItem.hovered || listUserItem.ListView.isCurrentItem)
                      ?Kirigami.Theme.highlightColor
                      :"transparent"

    }
    
    contentItem:RowLayout {

       spacing: 20

        Text {
            id: loginText
            text: listUserItem.login
            font.pointSize: 10
            elide: Text.ElideMiddle
            Layout.fillWidth: true
            Layout.preferredWidth: 300
            verticalAlignment: Text.AlignVCenter
        }

        ColumnLayout {
            id: userInfo
            spacing: 2
            Layout.fillWidth: true
            Layout.preferredWidth: 300
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
            Repeater {
                model: 4
                delegate: Rectangle {
                    width: 32; height:32
                    color: "transparent"
                    Image {
                        anchors.centerIn: parent
                        sourceSize.width: 32
                        sourceSize.height: 32
                        mipmap: true
                        smooth: true
                        source: listUserItem.pwdImgPaths[index] || ""
                        fillMode: Image.PreserveAspectFit
                    }
                }
            }
        }

        Button {
            id: manageUserBtn
            display: AbstractButton.IconOnly
            icon.name: "configure.svg"
            visible: listUserItem.ListView.isCurrentItem || listUserItem.hovered || optionsMenu.opened
            
            Layout.alignment: Qt.AlignVCenter
            Layout.preferredWidth: visible ? implicitWidth : 0
            
            ToolTip.delay: 1000
            ToolTip.timeout: 3000
            ToolTip.visible: hovered
            ToolTip.text: i18nd("easy-login","Click to manage this user")
            
            onClicked: optionsMenu.open()
            Connections{
                target:usersView
                function onCurrentIndexChanged(){
                    if (!listUserItem.ListView.isCurretItem && optionsMenu.opened){
                        optionsMenu.close()
                    }

                }
            }

            Menu {
                id: optionsMenu
                y: manageUserBtn.height
                x: -(width - manageUserBtn.width / 2)

                MenuItem {
                    text: i18nd("easy-login","Edit user")
                    icon.name: "document-edit.svg"
                    onClicked: userStackBridge.loadUser([username,pwdImgPaths])
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
