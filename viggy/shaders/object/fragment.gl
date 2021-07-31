# version 330 core


struct Material {
    float ambient_strength;
	float diffuse_strength;
	float specular_strength;
	float shininess;
};


struct Light {
    vec3 position;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    vec3 k;
};


in VS_OUT {
    vec3 position;
    vec2 UV;
    vec3 normal;
} fs_in;


uniform sampler2D texture;
uniform Material material;
uniform Light light;  // TODO: multiple lights
uniform vec3 camera_pos;


vec3 calc_light(Material material, Light light, vec3 frag_pos, vec3 camera_pos, vec3 normal)
{
	vec3 light_dir = normalize(light.position - frag_pos);
	vec3 camera_dir = normalize(camera_pos - frag_pos);
	vec3 reflected_light_dir = reflect(-light_dir, normal);

	float distance = length(light.position - frag_pos);
	float attenuation = 1.0 / (light.k.x + light.k.y * distance + light.k.z * distance * distance);

	float diffuse_factor = max(dot(normal, light_dir), 0.0f);
	float specular_factor = pow(max(dot(camera_dir, reflected_light_dir), 0.01f), material.shininess);

	vec3 ambience = material.ambient_strength * light.ambient;
	vec3 diffuse = material.diffuse_strength * diffuse_factor * light.diffuse;
	vec3 specular = material.specular_strength * specular_factor * light.specular;

	return (ambience + diffuse + specular) * attenuation;
}


void main()
{
    gl_FragColor = vec4(calc_light(material, light, fs_in.position, camera_pos, fs_in.normal), 1.0) *
                   texture(texture, fs_in.UV);
}
