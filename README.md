## Awards
Penapps 2022 winner: https://devpost.com/software/puppet

## Inspiration
Without purchasing hardware, there are few ways to have contact-free interactions with your computer. 
To make such technologies accessible to everyone, we created one of the first touch-less hardware-less means of computer control by employing machine learning and gesture analysis algorithms. Additionally, we wanted to make it as accessible as possible in order to reach a wide demographic of users and developers.

## What it does
Puppet uses machine learning technology such as k-means clustering in order to distinguish between different hand signs. Then, it interprets the hand-signs into computer inputs such as keys or mouse movements to allow the user to have full control without a physical keyboard or mouse.

## How we built it
Using OpenCV in order to capture the user's camera input and media-pipe to parse hand data, we could capture the relevant features of a user's hand. Once these features are extracted, they are fed into the k-means clustering algorithm (built with Sci-Kit Learn) to distinguish between different types of hand gestures. The hand gestures are then translated into specific computer commands which pair together AppleScript and PyAutoGUI to provide the user with the Puppet experience.

## Challenges we ran into
One major issue that we ran into was that in the first iteration of our k-means clustering algorithm the clusters were colliding. We fed into the model the distance of each on your hand from your wrist, and designed it to return the revenant gesture. Though we considered changing this to a coordinate-based system, we settled on changing the hand gestures to be more distinct with our current distance system. This was ultimately the best solution because it allowed us to keep a small model while increasing accuracy.   

Mapping a finger position on  camera to a point for the cursor on the screen was not as easy as expected. Because of inaccuracies in the hand detection among other things, the mouse was at first very shaky. Additionally, it was nearly impossible to reach the edges of the screen because your finger would not be detected near the edge of the camera's frame. In our Puppet implementation, we constantly _pursue_ the desired cursor position instead of directly _tracking it_ with the camera. Also, we scaled our coordinate system so it required less hand movement in order to reach the screen's edge.  

## Accomplishments that we're proud of
We are proud of the gesture recognition model and motion algorithms we designed. We also take pride in the organization and execution of this project in such a short time.

## What we learned
A lot was discovered about the difficulties of utilizing hand gestures. From a data perspective, many of the gestures look very similar and it took us time to develop specific transformations, models and algorithms to parse our data into individual hand motions / signs.

Also, our team members possess diverse and separate skillsets in machine learning, mathematics and computer science. We can proudly say it required nearly all three of us to overcome any major issue presented. Because of this, we all leave here with a more advanced skillset in each of these areas and better continuity as a team.

## What's next for Puppet
Right now, Puppet can control presentations, the web, and your keyboard. In the future, puppet could control much more.
- Opportunities in education: Puppet provides a more interactive experience for controlling computers. This feature can be potentially utilized in elementary school classrooms to give kids hands-on learning   with maps, science labs, and language.
- Opportunities in video games: As Puppet advances, it could provide game developers a way to create games wear the user interacts without a controller. Unlike technologies such as XBOX Kinect, it would require no additional hardware. 
- Opportunities in virtual reality: Cheaper VR alternatives such as Google Cardboard could be paired with 
Puppet to create a premium VR experience with at-home technology.  This could be used in both examples described above.
- Opportunities in hospitals / public areas: People have been especially careful about avoiding germs lately. With Puppet, you won't need to touch any keyboard and mice shared by many doctors, providing a more sanitary way to use computers.

## Credits
Project wouldnt be possible with Zayn Rekhi and Joey Sorkin who made this with me. They are not contributors to this repo since the orignal one was private.

