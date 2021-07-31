# version 330 core


// vertex attributes
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;  // need not be normalized
layout (location = 2) in vec2 UV;


// output to fragment
out VS_OUT {
    vec3 position;
    vec3 normal;
    vec2 UV;
} vs_out;


uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;


void main()
{
    // the position in world coordinates
    vs_out.position = (model * vec4(position, 1.0)).xyz;
    // the normal with model rotations but no translations
    vs_out.normal = normalize(mat3(model) * normal);
    vs_out.UV = UV;

    // the position in screen coordinates
    gl_Position = projection * view * vec4(vs_out.position, 1.0);
}
