# twack
Hacking your way to more twitter followers

## techniques

Follows [roughly this approach](https://mng.lincolnwdaniel.com/how-i-grew-from-300-to-5k-followers-in-just-3-weeks-2436528da845#.hjqoqzvr2)

Approach is this with awesome acronym SUCFWER

 1. seed with list of successful twitterers _T_ you want to emulate e.g. 5-10 people with 5k followers
 2. unfollow everyone who isn't following you already
 3. compute list _F_ of followers of guys in _T_, sorted by *most influental* (highest follower-friend ratio first)
 4. follow everyone in _F_ who is not already following you, as far as twitter allows (twitter has limits depending on your follower count)
 5. wait several days for followbacks from _F_
 6. (optional) expand _T_ by highly influental members of _F_ + _T_
 7. repeat at step 2

Doesn't work great unless people have a reason to follow you, e.g. you are a hot girl or you have high quality cryptocurrency rumors

## stack

Uses python, tweepy for the mechanics of the algorithm.
