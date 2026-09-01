

#=================================================================================#
#-----------------  Personal Shopping Assistant (E-commerce Agent)----------------#
#=================================================================================#

import asyncio
from agent import run_agent
from rag.run_ingestion import ingest_document
from tools.Retrieve_internal_documents import Retrieve_internal_documents


ingest_document("rag/RAGDataFiles/AI Engineer vs. ML Engineer.pdf")



# ====================== Call the Agent =======================#




response = asyncio.run( run_agent(
    #user_input="hello" ,
    #user_input="h" ,
    #user_input="what is the best Dell Latitude 5300 or Galaxy Book6 Ultra " ,
    #user_input="Recommend a gaming laptop and its accessories" ,
    #user_input="what are the reviews about HONOR Pad X9a ?" ,
    #user_input="i have an internship in ML what should i take it will be 6 months abroad in germany" ,
    #user_input="Find me the latest price of RTX 5070 laptops" ,
    #user_input="According to the uploaded PDF, what is the role of an AI Engineer?" ,
    user_input="from the uploaded file , how can i be an ML Engineer?" ,
    #-----------------------------------------
    #user_input="i can't decide what to buy, SKINOVA IMAGE Hair serum , Capixy Hair Serum , Leaves Hair Serum ?" ,
    #user_input"="i want a shampoo for dry hair." ,
    #user_input"="what does people say about essentials Moon Flower Dry Oil" ,
    #user_input=" what products have i had to go on a summer vacation " ,
    #user_input="how much does it cost to buy l'oreal paris hair mask ?" ,
    #-----------------------------------------------------
    #user_input="  recommend me a good korean nodles to cook with cheese souce ?" ,
    #user_input="  How much does it cost to buy korean ingradients to use at cooking ?" ,
    #user_input=" what is the best in Alfredo Sauce American Garden or Heinz  ?" ,
    

# users IDs 

            session_id = "customer_003"
            #-----------------------------
            #session_id= "customer_456"
            #-----------------------------
            #session_id="customer_789"
        
))


#print(response["output"])