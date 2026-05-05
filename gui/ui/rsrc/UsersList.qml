import org.kde.plasma.components as PC
import org.kde.kirigami as Kirigami
import QtQuick
import QtQuick.Controls
import QtQml.Models
import QtQuick.Layouts


Rectangle {
    property alias usersModel:filterModel.model
    property alias listCount:usersView.count
    color:"transparent"

    GridLayout{
        id:mainGrid
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        anchors.left:parent.left
        anchors.fill:parent
        RowLayout{
            Layout.alignment:Qt.AlignRight
            spacing:10
            PC.TextField{
                id:userSearchEntry
                font.pointSize:10
                horizontalAlignment:TextInput.AlignLeft
                Layout.alignment:Qt.AlignRight
                focus:true
                width:100
                visible:true
                enabled:{
                    if ((usersView.count==0)&& (text.length==0)) {
                        false
                    }else{
                        true
                    }
                }
                placeholderText:i18nd("easy-login","Search...")
                onTextChanged:{
                    filterModel.update()
                }
                
            }
        }

        Rectangle {
            id:usersList
            visible: true
            Layout.fillHeight:true
            Layout.fillWidth:true
            color:"white"
            border.color: "#d3d3d3"


            PC.ScrollView{
                implicitWidth:parent.width
                implicitHeight:parent.height
                anchors.leftMargin:10

                ListView{
                    id: usersView
                    anchors.fill:parent
                    height: parent.height
                    enabled:true
                    currentIndex:-1
                    clip: true
                    focus:true
                    boundsBehavior: Flickable.StopAtBounds
                    highlight: Rectangle { color: "#add8e6"; opacity:0.8;border.color:"#53a1c9" }
                    highlightMoveDuration: 0
                    highlightResizeDuration: 0
                    model:FilterDelegateModel{
                        id:filterModel
                        model:usersModel
                        role:"metaInfo"
                        search:userSearchEntry.text.trim()

                        delegate: ListDelegateUserItem{
                            width:usersList.width-18
                            username:model.username
                            login:model.login
                            name:model.name
                            surname:model.surname
                            pwdImg1:model.pwdImg1
                            pwdImg2:model.pwdImg2
                            pwdImg3:model.pwdImg3
                            pwdImg4:model.pwdImg4
                            metaInfo:model.metaInfo
                        }
                    }
                    Kirigami.PlaceholderMessage { 
                        id: emptyHint
                        anchors.centerIn: parent
                        width: parent.width - (Kirigami.Units.largeSpacing * 4)
                        visible: usersView.count==0?true:false
                        text: {
                            if (userSearchEntry.text.length==0){
                                i18nd("easy-login","No user is configured")
                            }else{
                                i18nd("easy-login","No user found")
                            }
                        }
                    }
                } 
             }
        }
    }
}

