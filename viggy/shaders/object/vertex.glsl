# version 330 core

// vertex attributes
layout (location = 0) in vec3 position;
layout (location = 1) in vec2 UV;
layout (location = 2) in vec3 normal;

// instance attributes
layout (location = 3) in vec3 i_position;

// output to geometry shader
out VS_OUT {
    vec3 position;
    vec2 UV;
    vec3 normal;
} vs_out;


uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;


void main()
{
    // the position in world coordinates
    vs_out.position = (model * vec4(position, 1.0)).xyz + i_position;
    vs_out.UV = UV;
    // the normal with model rotations but no translations
    vs_out.normal = normalize((mat4(mat3(model)) * vec4(normal, 1.0)).xyz);

    // the position in screen coordinates
    gl_Position = projection * view * vec4(vs_out.position, 1.0);
}
