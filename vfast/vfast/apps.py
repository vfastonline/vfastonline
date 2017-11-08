# encoding: utf8
from suit.apps import DjangoSuitConfig


class SuitConfig(DjangoSuitConfig):
    # layout这个参数决定你的网页是初始样式是垂直样式还是水平样式，可选参数为‘horizontal’或‘vertical’
    layout = 'vertical'
