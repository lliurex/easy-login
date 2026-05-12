import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQml.Models
import org.kde.plasma.components as PC
import org.kde.kirigami as Kirigami

Rectangle {
    id: root
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
                    
                    highlight: Rectangle { 
                        color: Kirigami.Theme.highlightColor
                        opacity: 0.3
                    }
                    highlightMoveDuration: 0
                    highlightResizeDuration: 0

                    Kirigami.PlaceholderMessage { 
                        anchors.centerIn: parent
                        width: parent.width - (Kirigami.Units.largeSpacing * 4)
                        visible: usersView.count === 0
                        text: userSearchEntry.text.length === 0
                              ? i18nd("easy-login", "There are no users configured")
                              : i18nd("easy-login", "No users where found")
                        icon.name:"group"
                    }
                } 
            }
        }
    }
}
