import streamlit as st

def styles_main():
   element_style = '''<style>
   #root > div:nth-child(1) > div.withScreencast > div > div > header{
   display: none}
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5{
   padding:0 !important;
   }
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(5),
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6){
   display: none
   }
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5{
   margin:0 20vw
   }
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div{
   gap:0 !important;}

   /* pading en dropdown genres */
   #complexnavbarSupportedContent ul li a {
      padding: 2px 1rem !important;
   }

   /*widht max */
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-13ln4jf.ea3mdgi5{
   max-width: 100vw !important}

   /* gap */
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div{
   gap:0 !important}

   /*  margin beetwen selected and posters */
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(12) > div > div > div{
   margin-bottom:10px}

   /* widht  */
   #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-gh2jqd.ea3mdgi5{
   max-width: none !important;
   padding-left: 1rem;
   padding-right: 1rem;
   }

/* title of the big fans */
#top-picks-for-our-biggest-fans{
   text-align: end;
    margin-bottom: 5px;
    padding: 0 !important;}

/*   margin in the title and checkbox */
#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(11){
margin-bottom: 22px !important}
    
/* margin of the checkbox */
#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(11) > div:nth-child(2) > div{
margin-top:10px !important}

/* label of checkbox */
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-uf99v8.ea3mdgi8 > div.block-container.st-emotion-cache-gh2jqd.ea3mdgi5 > div > div > div > div:nth-child(11) > div:nth-child(2) > div > div > div > div > div:nth-child(1) > div > div > div > div > div > label{
display: none !important;
}
/*  star inthe sidebar */
#root > div > ul{
      display: flex !important;
      justify-content: center !important;
      background-color:red !important};
/* marginin the check-box movie */
#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-gh2jqd.ea3mdgi5 > div > div > div > div:nth-child(11) > div:nth-child(2) > div > div > div > div > div{
margin-bottom: 10px !important}
/* login */
#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-gh2jqd.ea3mdgi5 > div > div > div > div.st-emotion-cache-0.eqpbllx5{
margin-top:2rem}
</style>
   '''
   st.markdown(element_style, unsafe_allow_html=True)   
# /* background img */
# #root > div:nth-child(1) > div.withScreencast > div > div > div > section {
#     background-image: url('https://i.imgur.com/SSPmAct.png') !important;
# }