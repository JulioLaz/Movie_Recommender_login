import pandas as pd
import ddbb
new_user=pd.read_csv('user_ratings.csv')
new_user['date'] = pd.to_datetime(new_user['date'])
new_user = new_user.loc[new_user.groupby(['movieId','userId'])['date'].idxmax()]
new_user= new_user[['userId','movieId','rating']]
# print(new_user)

max_user=ddbb.load_df_ratings()['userId'].max()

# if max_user <= 611:
#    print(max_user)
#    print(type(max_user))
#    print('nuevossss')

# new=new_user.userId.unique()[0]
# print('user:', new)