import random
# Open txt file
text_file = open('text.txt', 'r')
data = text_file.read()
text_file.close()
#print(data)



# Convert char/txt to bin
t2b = bin(int.from_bytes(data.encode(), 'big'));
#print(t2b)


inputs = t2b;
def v_xor(bit0,bit1):
    if(bit0==bit1):
        return '0'
    else:
        return '1'
def viterbi_encoder(inputs):
    #shift register encoder
    s_reg = ['0','0','0']
    obs = []
    for t in range (0,len(inputs)):
        #shifting the bits to right
        s_reg[2]=s_reg[1]
        s_reg[1]=s_reg[0]
        #inserting input
        s_reg[0]= inputs[t]
        state = s_reg[0]+ s_reg[1]
        obs.append([])
        #encoded bits
        obs[t] = v_xor(v_xor(s_reg[0],s_reg[1]),s_reg[2])+\
            v_xor(s_reg[0],s_reg[2])
    #    obs1 = ''.join(map(str, obs))
        #print(s_reg,state)
   #print(obs)
    #print codeword
    #print(obs1)
    #re-write list 'obs' as summable integers
    newlist = []
    # Check every item in list
    for item in obs:
      # If its a integer, add to newlist
      if isinstance(item, int):
        newlist.append(item)
        continue
      # else check and replace
      # evaluate branch combinations
      if '10' in item:
          item = item.replace('10', '1') # '10' = 1 + 0 = 1
      elif '01' in item:
          item = item.replace('01', '1') # '01' = 0 + 1 = 1
      elif '11' in item:
          item = item.replace('11', '2') # '11' = 1 + 1 = 2
      else:
          item = '0'                     # '00' = 0 + 0 = 0
     # Check other exception here
      
      newlist.append(int(item))
     
    #print(newlist)
    Sum = sum(newlist)
    #print(Sum)
    #Set even parity      
    if(Sum % 2 == 0):
          obs.insert(0,'0') #insert 0 bit if 'obs' is even
    else:
          obs.insert(0,'1') #insert 1 bit if 'obs' is odd
          
          
          
###################### Make this "real" dynamic BER ###########################
     # inject BER of 1.0E-8%    
    for i in range(0, len(obs)):
        if(Sum % 2 == 0) and random.randint(0,len(obs) < 1.0E-8):
              obs.insert(0,'1') #insert 1 bit if 'obs' is even
        else:
              obs.insert(0,'0') #insert 0 bit if 'obs' is odd
          
    #print(obs) #re-print fully constructed codewrod with parity bit
########################## Display bits flipped ###############################



    start_metric = {'zero':0,'one': 0, 'two': 0,'three':0}
    state_machine = {
        #current state, possible branches, branch information
        'zero': {'b1': {'out_b':"11",'prev_st': 'one','input_b':0},
                  'b2': {'out_b':"00",'prev_st': 'zero','input_b':0}},
        'one': {'b1': {'out_b': "01", 'prev_st': 'three', 'input_b': 0},
                  'b2': {'out_b': "10", 'prev_st': 'two', 'input_b': 0}},
        'two': {'b1': {'out_b': "11", 'prev_st': 'zero', 'input_b': 1},
                  'b2': {'out_b': "00", 'prev_st': 'one', 'input_b': 1}},
        'three': {'b1': {'out_b': "10", 'prev_st': 'three', 'input_b': 1},
                  'b2': {'out_b': "01", 'prev_st': 'two', 'input_b': 1}},
     
    }
     
    def bits_diff_num(num_1,num_2): #convolved signal, num_1=original data, num_2 = codeword
        count=0;
        for i in range(0,len(num_1),1):
            if num_1[i]!=num_2[i-1]:
                count=count+1
        return count
    
    #Error detectection
    #Error correction
     
    def viterbi_decoder(obs, start_metric, state_machine):
        #Trellis structure
        V = [{}]
        for st in state_machine:
            # Calculating the probability of both initial possibilities for the first observation
            V[0][st] = {"metric": start_metric[st]}
        #for first_b_metric > second_b_metric
        for t in range(1, len(obs)+1):
            V.append({})
            for st in state_machine:
                #Check for smallest bit difference from possible previous paths, adding with previous metric
                prev_st = state_machine[st]['b1']['prev_st']
                first_b_metric = V[(t-1)][prev_st]["metric"] + bits_diff_num(state_machine[st]['b1']['out_b'], obs[t - 1])
                prev_st = state_machine[st]['b2']['prev_st']
                second_b_metric = V[(t - 1)][prev_st]["metric"] + bits_diff_num(state_machine[st]['b2']['out_b'], obs[t - 1])
                #print(state_machine[st]['b1']['out_b'],obs[t - 1],t)
                if first_b_metric > second_b_metric:
                    V[t][st] = {"metric" : second_b_metric,"branch":'b2'}
                else:
                    V[t][st] = {"metric": first_b_metric, "branch": 'b1'}
     
        #print trellis nodes metric:
        for st in state_machine:
            for t in range(0,len(V)):
                #print(V[t][st],["metric"])
            #print(""),
        #print(""),
     
        smaller = min(V[t][st]["metric"] for st in state_machine)
        #traceback the path on smaller metric on last trellis column
        for st in state_machine:
         if V[len(obs)-1][st]["metric"] == smaller:
             source_state = st
             for t in range(len(obs),0,-1):
                 branch = V[t][source_state]["branch"]
                 #print(state_machine[source_state][branch]['input_b']),
                 source_state = state_machine[source_state][branch]['prev_st']
                 #print (source_state+"\n")
                 #print("Finish")
                 
                 
             

     
    viterbi_decoder(obs,
            start_metric,
            state_machine)
    

viterbi_encoder(inputs)

b2t = int(str(inputs), 2)
         
             
text = b2t.to_bytes((b2t.bit_length() + 7) // 8, 'big').decode()
print(text)   
    