import streamlit as st

def line_gold():
   css = """
   <style>
   @keyframes gradient {
      0% {
         background-position: 0% 50%;
      }
      50% {
         background-position: 100% 50%;
      }
      100% {
         background-position: 0% 50%;
      }
   }

   .gold-line {
      margin-top:10px;
      margin-bottom:20px;
      width: 100%;
      height: 10px;
      background: linear-gradient(270deg, #FFD700, #FFEC8B, #cfad04);
      background-size: 600% 600%;
      animation: gradient 3s ease infinite;
   }
   </style>
   """
   st.markdown(css, unsafe_allow_html=True)
   st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)