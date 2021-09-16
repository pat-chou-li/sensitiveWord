from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.commons.utils import JsCode
data_x = ['可乐', '雪碧', '橙汁', '绿茶', '奶茶', '百威', '青岛']
data_y = [47, 53, 27, 23, 94, 18, 48]
c = (
    Bar()
    .add_xaxis(data_x)
    .add_yaxis("商家A", data_y, category_gap="60%")
    .set_series_opts(
        itemstyle_opts={
            "normal": {
                "color": JsCode(
                    """new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: 'rgba(0, 244, 255, 1)'
            }, {
                offset: 1,
                color: 'rgba(0, 77, 167, 1)'
            }], false)"""
                ),
                "barBorderRadius": [30, 30, 30, 30],
                "shadowColor": "rgb(0, 160, 221)",
            }
        }
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="销量"),
                     xaxis_opts=opts.AxisOpts(
        name='类别',
        name_location='middle',
        name_gap=30,  # 标签与轴线之间的距离，默认为20，最好不要设置20
        name_textstyle_opts=opts.TextStyleOpts(
            font_family='Times New Roman',
            font_size=16  # 标签字体大小
        )),
        yaxis_opts=opts.AxisOpts(
        name='数量',
        name_location='middle',
        name_gap=30,
        name_textstyle_opts=opts.TextStyleOpts(
            font_family='Times New Roman',
            font_size=16
            # font_weight='bolder',
        )),
        # toolbox_opts=opts.ToolboxOpts()  # 工具选项
    )
    .render("水晶柱状图.html")
)
print(c)
