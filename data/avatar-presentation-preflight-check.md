# Avatar preflight checklist

1. Weighted to 4 bone weights and range of motion doesn't break the skinning
1. Add shader motion
1. [TaSTT](https://github.com/yum-food/TaSTT)'s text player
1. Overly bright lights don't make the avatar's surface glow.
1. The body mesh must be intact -- Parts of the body MUST not be removed.
1. VRM0 materials
1. VRM0 spring bones
1. 52 blend shapes for the face
1. Gut feel check

## glTF - VRM Version 0 Performance Rank Limits

| Avatar Quality                            | Poor         |
| ----------------------------------------- | ------------ |
| Primitives (Mesh Complexity)              | 70000       |
| Bounds Size (Model Scale)                 | 5m x 6m x 5m |
| Texture Memory (Texture Size)             | 150 MB       |
| Morph Targets (Blendshape Amount)         | 16           |
| Meshes (Mesh Count)                       | 24           |
| Materials (Material Count)                | 32           |
| Secondary Animation Components            | 32           |
| Secondary Animation Affected Nodes        | 256          |
| Secondary Animation Collision Check Count | 512          |
| Animations                                | 32           |
| Joints (Joint Count)                      | 400          |
| Lights                                    | 1            |
| Spring Bones                              | 32           |

## Mobile Medium Performance Rank Limits

| Attribute                       | Limit        |
| ------------------------------- | ------------ |
| Polygons                        | 15,000       |
| Bounds Size                     | 5m x 6m x 5m |
| Texture Memory                  | 25 MB        |
| Skinned Meshes                  | 2            |
| Meshes                          | 2            |
| Material Slots                  | 2            |
| Animators                       | 1            |
| Bones                           | 150          |
| PhysBones Components            | 6            |
| PhysBones Affected Transforms   | 32           |
| PhysBones Colliders             | 8            |
| PhysBones Collision Check Count | 32           |
| Avatar Dynamics Contacts        | 8            |
| Particle Systems                | 0            |
| Total Particles Active          | 0            |
| Mesh Particle Active Polys      | 0            |
| Particle Trails Enabled         | False        |
| Particle Collision Enabled      | False        |
| Trail Renderers                 | 0            |
| Line Renderers                  | 0            |

## PCVR Poor Performance Rank Limits

| Avatar Quality                     | Poor         |
| ---------------------------------- | ------------ |
| Polygons                           | 70,000       |
| Bounds Size                        | 5m x 6m x 5m |
| Texture Memory                     | 150 MB       |
| Skinned Meshes                     | 16           |
| Meshes                             | 24           |
| Material Slots                     | 32           |
| Dynamic Bone Components            | 32           |
| Dynamic Bone Transforms            | 256          |
| Dynamic Bone Colliders             | 32           |
| Dynamic Bone Collision Check Count | 256          |
| PhysBones Components               | 32           |
| PhysBones Affected Transforms      | 256          |
| PhysBones Colliders                | 32           |
| PhysBones Collision Check Count    | 512          |
| Avatar Dynamics Contacts           | 32           |
| Animators                          | 32           |
| Bones                              | 400          |
| Lights                             | 1            |
| Particle Systems                   | 16           |
| Total Particles Active             | 2500         |
| Mesh Particle Active Polys         | 5000         |
| Particle Trails Enabled            | True         |
| Particle Collision Enabled         | True         |
| Trail Renderers                    | 8            |
| Line Renderers                     | 8            |
| Cloths                             | 1            |
| Total Cloth Vertices               | 200          |
| Physics Colliders                  | 8            |
| Physics Rigidbodies                | 8            |
| Audio Sources                      | 8            |
