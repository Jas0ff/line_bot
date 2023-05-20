from linebot.models import *
import db


method_choose = TemplateSendMessage(
  alt_text='歡迎選擇',
  template=CarouselTemplate(
    columns=[
      # CarouselColumn(
      #   thumbnail_image_url='https://images.unsplash.com/photo-1589476993333-f55b84301219?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=327&q=80',
      #   title='抽獎',
      #   text= f'為了獎項而加入,目前有{db.get_lottery_people_num()}人參加抽獎',
      #   actions=[
      #     PostbackAction(
      #         label='這我',
      #         display_text='-----已選擇:抽獎, 請稍後----',
      #         data='lottery'
      #     )
      #   ]
      # ),
      CarouselColumn(
        thumbnail_image_url='https://plus.unsplash.com/premium_photo-1677094310893-0d6594c211ea?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1032&q=80',
        title='虛擬AI寶貝',
        text='單身專屬',
        actions=[
          PostbackAction(
              label='輕觸以激活您的小寶貝',
              display_text='-----已選擇:AI寶貝, 請稍後----',
              data='aichat'
          )
        ]
      ),
      CarouselColumn(
        thumbnail_image_url='https://images.unsplash.com/photo-1586095087956-bc66fe634955?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=466&q=80',
        title='心情歌單',
        text='推薦符合你現在心情的歌',
        actions=[
          PostbackAction(
              label='狙擊你的心靈歌曲',
              display_text='-----已選擇:心情歌單, 請稍後----',
              data='moodsong'
          )
        ]
      )
    ]
  )
)