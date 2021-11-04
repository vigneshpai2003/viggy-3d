# version 330 core


struct Material {
    vec3 ambient;
	vec3 diffuse;
	vec3 specular;
	float shininess;  // affects radius of specular highlight
};


struct Light {
    vec3 position;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;

    vec3 k;  // attenuation
};


in VS_OUT {
    vec3 position;
    vec3 normal;  // already normalized
    vec2 UV;
} fs_in;


uniform sampler2D baseTexture;
uniform Material material;
uniform Light light;

uniform vec3 cameraPos;


vec3 calcLight(Material _material,
               Light _light,
               vec3 _fragPos,  // position of fragment in world coordinates
               vec3 _cameraPos,  // position of camera in world coordinates
               vec3 _normal)  // normalized normal
{
    // ambient
    vec3 ambient = _light.ambient * _material.ambient;

    // diffuse
	vec3 lightDir = normalize(_light.position - _fragPos);
	float diffuseFactor = max(dot(_normal, lightDir), 0.0f);
	vec3 diffuse = diffuseFactor * _light.diffuse * _material.diffuse;

	// specular
	vec3 cameraDir = normalize(_cameraPos - _fragPos);
    vec3 reflectedDir = reflect(-lightDir, _normal);
    float specularFactor = pow(max(dot(cameraDir, reflectedDir), 0.01f), _material.shininess);
    vec3 specular = specularFactor * _light.specular * _material.specular;

    // loss in light due to distance
	float distance = length(light.position - _fragPos);
	float attenuation = 1.0 / (light.k.x + light.k.y * distance + light.k.z * distance * distance);

	return (ambient + diffuse + specular) * attenuation;
}


void main()
{
    gl_FragColor = vec4(calcLight(material, light, fs_in.position, cameraPos, fs_in.normal), 1.0) *
                   texture(baseTexture, fs_in.UV);
}
