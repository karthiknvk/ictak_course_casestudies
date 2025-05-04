from flask import Flask,request,render_template,redirect
import pickle
import numpy as np
# FLASK WEB APP
app=Flask(__name__)
model=pickle.load(open('PHISHING_model.pkl','rb'))
@app.route('/')
def home():
  return render_template("home.html",)
# WEB APP
@app.route('/check',methods=['POST'])
def check():
  url_name=request.values['url_name']
  domain_name=request.values['domain_name']
  ext_ref=request.values['ext_ref']
  line_of_code=request.values['line_of_code']
  self_ref=request.values['self_ref']
  images=request.values['images']
  js_count=request.values['js_count']
  is_social_net=request.values['is_social_net']
  css_count=request.values['css_count']
  has_copyright_info=request.values['has_copyright_info']
  len_large_line=request.values['len_large_line']
  has_description=request.values['has_description']
# IS SOCIAL NETOWRK
  if is_social_net=="YES":
    is_social_net=1
  else:
    is_social_net=0  
# HAS COPY_RIGHT_INFO
  if has_copyright_info=="YES":
    has_copyright_info=1
  else:
    has_copyright_info=0
# HAS DESCRIPTION  
  if has_description=="YES":
    has_description=1
  else:
    has_description=0
# IS HTTPS:
  part1 = url_name.split("//")[0]
  if part1=="https:":
    is_https=1
  else:
    is_https=0
# URL SIMILARITY INDEX
  part2 = url_name.split("//")[1]
  if part2==domain_name:
    URL_SIMILARITY_INDEX = 1
  else:
    URL_SIMILARITY_INDEX = 0
# ENTER DETAILS
  print(f"url_name            ->{url_name}")
  print(f"domain_name         ->{domain_name}")
  print(f"ext_ref             -> {ext_ref}")
  print(f"line_of_code        ->{line_of_code}")
  print(f"self_ref            ->{self_ref}")
  print(f"images              ->{images}")
  print(f"js_count            ->{js_count}")
  print(f"is_social_net       ->{is_social_net}")
  print(f"css_count           ->{css_count}")
  print(f"has_copyright_info  ->{has_copyright_info}")
  print(f"len_large_line      ->{len_large_line}")
  print(f"has_description     ->{has_description}")
# ENTERED VALUED
  values_taken=[URL_SIMILARITY_INDEX,
                ext_ref, 
                line_of_code, 
                self_ref, 
                images, 
                js_count, 
                is_social_net,
                css_count,
                has_copyright_info,
                len_large_line,
                has_description]
  
  """  
  //CODE FOR PREDICTING WITH MODEL   
  """
  features = np.array([[URL_SIMILARITY_INDEX, ext_ref, line_of_code, self_ref, images, js_count, is_social_net,css_count,has_copyright_info,is_https,len_large_line,has_description ]])
  prediction = model.predict(features)
  result = prediction
# RESULT
  if result==0:
    result_display=f"IT MIGHT BE A PHISHING URL"
  else:
    result_display=f"IT MIGHT NOT BE A PHISHING URL"

  return render_template("result.html",values_taken=values_taken,result_display=result_display)
# WEB APP EXECUTION
if __name__=='__main__':
  app.run(debug=True)
