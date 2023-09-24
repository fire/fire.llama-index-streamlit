# What is VRM ? What can VRM do ?

![VRM](https://vrm.dev/en/vrm/vrm_about.html)

VRM is a versatile tool that can handle humanoid character avatars.

- It provides a standard implementation (UniVRM) for reading and writing VRM files in Unity
  - [Download UniVRM](https://github.com/vrm-c/UniVRM/releases)
- The format is glTF based, so it’s cross-platform. It can also be handled by other game engines and the Web.
  - [Learn more about glTF](https://www.khronos.org/gltf/)

## Contents

- VRM is formulated on top of the 3D standard format glTF2.0 to handle the humanoid model. The humanoid motion (e.g. from motion capture) can be reproduced based on defined Humanoid bones in VRM

- Runtime VRM Import: all data including textures and materials is compacted as one file. To import the VRM model into applications, only one single file is needed

- Standard face operations such as emotions, blinks, and aiueo are defined, and you can do the following:

  - Select facial expressions by user operation
  - Lip sync from voice
  - Random blink
  - Assign facial capture
  - [Learn more about BlendShape](https://docs.unity3d.com/Manual/BlendShapes.html)

- It supports 3 types of materials (shaders):

  - [PBR](https://en.wikipedia.org/wiki/Physically_based_rendering)
  - [Unlit](https://docs.unity3d.com/Manual/shader-StandardUnlit.html)
  - [MToon](https://github.com/Santarh/MToon)

- It supports 3 types of line-of-sight control:

  - Gaze by Bone
  - Gaze by BlendShape
  - Gaze by TextureUV

- There is a standard implementation of swaying objects that does not depend on the physics engine, such as the character’s hair.

  - [Learn more about SpringBone](https://github.com/vrm-c/UniVRM/blob/master/Assets/VRM/UniVRM/Scripts/SpringBone/README.md)

- Avatar’s first-person view is available in VR

  - [Learn more about FirstPerson](https://docs.unity3d.com/Manual/class-Camera.html)

- Despite the Meta information such as Model Title and Author Name, with the advent of the VR era, Thumbnail and License Information are also included in the VRM file.
  - [Learn more about Meta](https://vrm.dev/en/docs/univrm/meta/)

As described above, VRM is not just a 3D model data. It is designed for being able to be used right away once being loaded into applications.

## What can you do with VRM?

The same avatar (VRM model) data can be used in any application that supports VRM. As long as various VRM applications are made, the future will look like the one described below for sure…

- Create your own avatar with the character maker in VRM format
- Use your own avatar to host a live streaming event and show up on your friends’ live channels
- After the live streaming, start a VR game to explore the VR world with your own avatar
- After the game, move to the chat room in the VR world. Use the same avatar character to hang out with friends
- Tomorrow join the VR study group in VR. Of course, the same avatar appearance

By using your own avatar (3D model data) in VRM format, you can access various applications and games that support VRM.

Live streaming, video creation, games, chat…. The virtual worlds are not connected with each other. Using VRM is the first step to bridge those virtual worlds

## VRM applications

- [Applications that support VRM](https://vrm.dev/en/vrm_applications/)

## VRM features

In the past, handling 3D humanoid avatar (3D model) in Virtual Reality, Virtual YouTuber, etc. was not trivial as it was necessary to develop unique systems for applications and fine-tune the 3D model data due to:

- The output data is depend on how creators make the 3D model and what modeling tools are used

  - The coordinate system, scale, initial pose, and the way to express expressions are all different…
  - Needless to say, the way bones put into the 3D model is also different
  - The initial posture is different (T-Pose, A-Pose, Z + orientation, Z-direction).
  - The expression method of facial expressions is different (Morph, Bone, identification method).
  - Needless to say, the way bones put into the 3D model is also different

- Each company has its own specifications for handling the 3D model data, which are way more complex than usual. Also, the necessary information about their file formats is not fully provided

  - Whether the FBX file, which is compatible with various software, is viable for an application and which version of the application can process the FBX file are main issues concerned by most of the users.
  - Game engines can be captured as assets, but run-time loading is often not expected.

- There is not enough necessary information available from the viewpoint of using the 3D model data as Avatar
  - For example, in the first-person view, how to get the right viewpoint position, how to exclude head due to the view blocking issue and so on

With the use of avatar in VR applications grows exponentially, if the situations mentioned above remain unchanged, application developers and 3D model creators will have to spend double or triple effort. To improve the current situation, based on the humanoid character and avatar, we can do the followings:

- In Humanoid Characters and Avatar
  - Effectively absorb and unify the differences from the model data
  - Make handling the 3D model easy on the application side

Here we propose a platform-independent, 3D avatar file format called VRM that has the above features.
