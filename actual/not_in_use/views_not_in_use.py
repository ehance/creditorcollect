#nvd3 not currently used
from django.shortcuts import render_to_response
def demo_piechart(request):
    """
    pieChart page
    """
    xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries",
             "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]

    color_list = ['#5d8aa8', '#e32636', '#efdecd', '#ffbf00', '#ff033e', '#a4c639',
                  '#b2beb5', '#8db600', '#7fffd4', '#ff007f', '#ff55a3', '#5f9ea0']
    extra_serie = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "color_list": color_list
    }
    chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'  # container name
    chartdata1 = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
    charttype1 = "lineChart"
    chartcontainer1 = 'linechart_container'  # container name

    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
    	'charttype1': charttype1,
        'chartdata1': chartdata1,
        'chartcontainer1': chartcontainer1,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    return render_to_response('piechart.html', data)

def demo_chart(request):
    """
    demo_chart page
    """

    xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries",
             "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]

    color_list = ['#5d8aa8', '#e32636', '#efdecd', '#ffbf00', '#ff033e', '#a4c639',
                  '#b2beb5', '#8db600', '#7fffd4', '#ff007f', '#ff55a3', '#5f9ea0']
    extra_serie = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "color_list": color_list,
    }
    chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie, 'xRange': [0, 1000000]}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'  # container name
    chartdata1 = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
    charttype1 = "lineChart"
    chartcontainer1 = 'linechart_container'  # container name

    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
    	'charttype1': charttype1,
        'chartdata1': chartdata1,
        'chartcontainer1': chartcontainer1,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }

    data = output_nvd3.charts(name ='Average Assets')
    return render_to_response('demo_chart.html', data)

# Div(Field('age'),
#     Field('gender_male'),
#     Field('health'),
#     Field('smoker'),
#     Field('leisure'),
#     Field('annual_income'),
#     # Field('discount'),
#     Field('bequest'), css_class='col-xs-6'),
# Div(
#     Field('assets_trad_ira'),
#     Field('assets_roth_ira'),
#     Field('assets_mutual_funds'),
#     Field('assets_annuities'),
#     Field('assets_acccounts'),
#     Field('assets_other'),
#     Field('risk_aversion_investment'),

    # my_inputs = inputs(user.profile.percent_to_invest, user.profile.age, user.profile.retirement_age, user.profile.risk_aversion, user.profile.mortality_factor, user.profile.annual_consumption,  user.profile.annual_income, user.profile.cash,
    #                    user.profile.bonds, user.profile.equities,user.profile. bequest_utility_factor)
