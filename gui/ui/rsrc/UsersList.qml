import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQml.Models
import org.kde.plasma.components as PC
import org.kde.kirigami as Kirigami

Rectangle {
    id: usersListContainer
    property alias usersModel: filterModel.model
    property alias listCount: usersView.count
    color: "transparent"

    ColumnLayout { 
        anchors.fill: parent
        spacing: 10

        RowLayout {
            Layout.fillWidth: true
            Item { Layout.fillWidth: true }

            PC.TextField {
                id: userSearchEntry
                placeholderText: i18nd("easy-login", "Search...")
                Layout.preferredWidth: 150
                enabled: usersView.count > 0 || text.length > 0
           }
        }

        Rectangle {
            id: usersList
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "white"
            border.color: "#d3d3d3"
            border.width: 1

            PC.ScrollView {
                anchors.fill: parent

                ListView {
                    id: usersView

                    Timer {
                        id: searchTimer
                        interval: 150
                        repeat: false
                        onTriggered: filterModel.update()
                    }
                    
                    model: FilterDelegateModel {
                        id: filterModel
                        model: usersModel
                        role: "metaInfo"
                        search: userSearchEntry.text.trim()

                        externalTimer: searchTimer 

                        delegate: ListDelegateUserItem {
                            width: usersView.width
                            username: model.username
                            login: model.login
                            name: model.name
                            surname: model.surname
                            pwdImgPaths: model.pwdImgPaths
                            metaInfo: model.metaInfo
                        }
                    }
                    
                    currentIndex: -1
                    clip: true
                    focus: true
                    boundsBehavior: Flickable.StopAtBounds
                    
                    highlightFollowsCurrentItem:true
                    highlightMoveDuration: 0
                    highlightResizeDuration: 0

                    highlight: Item{
                        width:usersView.width
                        height:usersView.currentItem?usersView.currentItem.height:70
                        Rectangle {
                            x:5
                            y:5
                            width:parent.width-10
                            height:parent.height-5 
                            color: Qt.alpha(Kirigami.Theme.highlightColor,0.15)
                            radius:6
                            border.width:1
                            border.color:Kirigami.Theme.highlightColor

                        }
                    }

                    Kirigami.PlaceholderMessage { 
                        anchors.centerIn: parent
                        width: parent.width - (Kirigami.Units.largeSpacing * 4)
                        visible: usersView.count === 0
                        text: userSearchEntry.text.length === 0
                              ? i18nd("easy-login", "There are no users configured")
                              : i18nd("easy-login", "No users where found")
                        icon.name:"easy-login"
                    }
                } 
            }
        }
    }
}
