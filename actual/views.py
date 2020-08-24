from django.views import generic
import calc_engine
import calc_engine.output_matplotlib as output_matplotlib
import calc_engine.helper as helper
import time

### move to templatetag folder
# from django import template
# register = template.Library()
#
# # you might want to use simple_tag if you are on 1.9 or higher version
# @register.assignment_tag
# def to_list(*args):
#     return args


class HomePage(generic.TemplateView):
  template_name = "home.html"


class FiduciaryPage(generic.TemplateView):
  template_name = "fiduciary.html"


class TeamPage(generic.TemplateView):
  template_name = "team.html"

class TradierAccountOpenedPage(generic.TemplateView):
  template_name = "tradier-account-opened.html"


class PricingPage(generic.TemplateView):
  template_name = "pricing.html"


from django.shortcuts import render

'''to do, generalize better'''

def plan(request):
  context = {}
  faq_list(context)
  #if request.user.profile.age is None:
  context['age'] = request.user.profile.age #'Please update your profile'
  return render(request, 'plan/plan.html', context)

def assets(request):
  context = {}
  faq_list(context)
  return render(request, 'plan/assets.html', context)

def spending(request):
  context = {}
  faq_list(context)
  return render(request, 'plan/spending.html', context)

def estate(request):
  calc_object = get_calc_object(request)
  context = {
    'average_estate': helper.as_currency(calc_object.average('bequest')),
    'target_estate': helper.as_currency(calc_object.bequest_threshold),
    'percent_below_target_estate': helper.as_percent(calc_object.below('bequest', calc_object.bequest_threshold)),
    'median_age': calc_object.median_age(),
    'survive_past_90': helper.as_percent(calc_object.mortality.survive_until_age(90)),
  }
  faq_list(context)
  return render(request, 'plan/estate.html', context)

def liquidity(request):
  context = {}
  faq_list(context)
  return render(request, 'plan/liquidity.html', context)

def utility(request):
  context = {}
  faq_list(context)
  return render(request, 'plan/utility.html', context)

def actions(request):
  calc_object = get_calc_object(request)
  context = {
    'savings_rate': helper.as_percent(calc_object.optimal['savings_rate']),
    'ret_age': calc_object.optimal['ret_age'],
    'wd_rate': helper.as_percent(calc_object.optimal['wd_rate']),
    'US_stocks': helper.as_percent(calc_object.optimal_equity / 2),
    'International_stocks': helper.as_percent(calc_object.optimal_equity / 2),
    'bonds': helper.as_percent(1 - calc_object.optimal_equity),
    'inflation_rate': helper.as_percent(calc_object.market.inflation),
    # 'US_stocks': helper.as_percent(calc_object.optimal['equity_allocation']/2),
    # 'International_stocks': helper.as_percent(calc_object.optimal['equity_allocation']/2),
    # 'bonds': helper.as_percent(1 - calc_object.optimal['equity_allocation']),
    # 'US_stocks': helper.as_percent(calc_object.optimal['investment_allocation']['equities']/2.),
    # 'International_stocks': helper.as_percent(calc_object.optimal['investment_allocation']['equities']/2.),
    # 'bonds': helper.as_percent(calc_object.optimal['investment_allocation']['bonds']),
    # 'investment_allocation': ' {investment_allocation} ',
    # 'investment_allocation': helper.as_percent(calc_object.optimal['investment_allocation']['equities']/2.),
    # 'investment_allocation': helper.as_percent(calc_object.optimal['investment_allocation']['equities']/2.) + " US stocks" +
    #                          helper.as_percent(calc_object.optimal['investment_allocation']['equities']/2.) + " International stocks" +
    #                          helper.as_percent(calc_object.optimal['investment_allocation']['bonds']) + " bonds",
    # 'faq_list': ['student_loan'],
  }
  faq_list(context)
  return render(request, 'plan/actions.html', context)

def investing(request):
  context = {}
  faq_list(context)
  return render(request, 'plan/investing/investing.html', context)

def faq_list(context):
  import glob, os
  faq_list = []
  for filename in glob.iglob('templates/plan/faq/*.html'):
    faq_list.append(os.path.basename(filename))
  context['faq_list'] = faq_list

def faq(request, name):
  context = {
    'income': request.user.profile.annual_income,
    'age': request.user.profile.age,
    'name': name,
  }
  faq_list(context)
  return render(request, 'base_faq.html', context)
  # return render(request, 'plan/faq/' + name + '.html')

def open_matplotlib():
  if output_matplotlib.threads_in_matplotlib == 0:
    output_matplotlib.threads_in_matplotlib += 1
    return
  else:
    # sleep until there are no threads opening matplotlib
    time.sleep(0.1)
    open_matplotlib()


def close_matplotlib():
  output_matplotlib.threads_in_matplotlib -= 1
  return

def chart(request, name=''):
  # output_matplotlib.threads_in_matplotlib = 0
  # inputs = {}
  # inputs['age'] = request.user.profile.age
  # inputs['assets'] = request.user.profile.assets_acccounts + request.user.profile.assets_annuities + request.user.profile.assets_mutual_funds + \
  #          request.user.profile.assets_other + request.user.profile.assets_roth_ira + request.user.profile.assets_trad_ira
  # inputs['income'] = request.user.profile.annual_income
  # inputs['leisure'] = request.user.profile.leisure
  # inputs['smoker'] = request.user.profile.smoker
  # inputs['bequest'] = request.user.profile.bequest / 10000    #based on how question is framed
  # inputs['gender'] = request.user.profile.gender_male
  # inputs['health'] = request.user.profile.health
  # inputs['risk_aversion'] = request.user.profile.risk_aversion_investment
  #
  # import calc_engine.global_settings
  # for key in set(calc_engine.global_settings.DEFAULT_CUSTOMER_INPUTS.keys()) - set(inputs.keys()):
  #     inputs[key] = calc_engine.global_settings.DEFAULT_CUSTOMER_INPUTS[key]
  #
  # import calc_engine.main
  # __, calc_object = calc_engine.main.main(**inputs)   #to do, cache by user
  calc_object = get_calc_object(request)

  name = str(name).replace("_", " ")

  # matplotlib has a multi-threading issue where if multiple graphs are plotted on the same html page unless do below
  open_matplotlib()
  response = output_matplotlib.charts(calc_object=calc_object, name=name)
  close_matplotlib()

  # to do: look at threads and only let the thread highest on the webpage plot first, so plots are rendered in expected top/down order

  return response


def get_inputs(request):
  inputs = {}
  inputs['age'] = request.user.profile.age
  inputs['assets'] = request.user.profile.assets_acccounts + request.user.profile.assets_annuities + request.user.profile.assets_mutual_funds + \
                     request.user.profile.assets_other + request.user.profile.assets_roth_ira + request.user.profile.assets_trad_ira
  inputs['income'] = request.user.profile.annual_income #assumes spending includes taxes
  inputs['leisure'] = request.user.profile.leisure / 100. * request.user.profile.annual_income
  inputs['smoker'] = request.user.profile.smoker
  inputs['bequest'] = request.user.profile.bequest / 10000  # based on how question is framed
  inputs['gender'] = request.user.profile.gender_male
  inputs['health'] = request.user.profile.health
  inputs['risk_aversion'] = request.user.profile.risk_aversion_investment

  for key in set(calc_engine.global_settings.DEFAULT_CUSTOMER_INPUTS.keys()) - set(inputs.keys()):
    inputs[key] = calc_engine.global_settings.DEFAULT_CUSTOMER_INPUTS[key]
  return inputs


def get_calc_object(request):
  __, c = calc_engine.main.main(**get_inputs(request))
  return c


# not used yet
def update_calc_object(request):
  inputs = {}
  inputs['age'] = request.user.profile.age
  inputs['assets'] = request.user.profile.assets_acccounts + request.user.profile.assets_annuities + request.user.profile.assets_mutual_funds + \
                     request.user.profile.assets_other + request.user.profile.assets_roth_ira + request.user.profile.assets_trad_ira
  inputs['income'] = request.user.profile.annual_income
  inputs['leisure'] = request.user.profile.leisure
  inputs['smoker'] = request.user.profile.smoker
  inputs['bequest'] = request.user.profile.bequest / 10000  # based on how question is framed
  inputs['gender'] = request.user.profile.gender_male
  inputs['health'] = request.user.profile.health
  inputs['risk_aversion'] = request.user.profile.risk_aversion_investment

  import calc_engine.global_settings
  for key in set(calc_engine.global_settings.DEFAULT_CUSTOMER_INPUTS.keys()) - set(inputs.keys()):
    inputs[key] = calc_engine.global_settings.DEFAULT_CUSTOMER_INPUTS[key]
  txt = ""
  for key in inputs.keys():
    txt += str(key) + " " + str(inputs[key]) + " "
  context = {}
  context['txt'] = txt

  import calc_engine.main
  return calc_engine.main.main(**inputs)  ####***** return calc_object then pass to output_matplotlib


def test_user_info(request):
  inputs = {}
  inputs['age'] = request.user.profile.age
  inputs['assets'] = request.user.profile.assets_acccounts + request.user.profile.assets_annuities + request.user.profile.assets_mutual_funds + \
                     request.user.profile.assets_other + request.user.profile.assets_roth_ira + request.user.profile.assets_trad_ira
  inputs['income'] = request.user.profile.annual_income
  inputs['leisure'] = request.user.profile.leisure
  inputs['smoker'] = request.user.profile.smoker
  inputs['bequest'] = request.user.profile.bequest / 10000  # based on how question is framed
  inputs['gender'] = request.user.profile.gender_male
  inputs['health'] = request.user.profile.health
  inputs['risk_aversion'] = request.user.profile.risk_aversion_investment

  import calc_engine.global_settings
  for key in set(calc_engine.global_settings.DEFAULT_CUSTOMER_INPUTS.keys()) - set(inputs.keys()):
    inputs[key] = calc_engine.global_settings.DEFAULT_CUSTOMER_INPUTS[key]
  txt = ""
  for key in inputs.keys():
    txt += str(key) + " " + str(inputs[key]) + " "
  context = {}
  context['txt'] = txt

  import calc_engine.main
  __, calc_engine.output_matplotlib.calc_object = calc_engine.main.main(**inputs)

  return render(request, 'test/user_info.html', context=context)


'''
to do:
Cache calc objects by user to speed up loading of graphs
Have user questions address missing variables
'''
