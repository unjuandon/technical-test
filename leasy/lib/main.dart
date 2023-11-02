import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  runApp(MyApp());
}

class Property {
  final String name;
  final String address;
  final String propertyType;
  final String image;

  Property(this.name, this.address, this.propertyType, this.image);
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final TextEditingController nameController = TextEditingController();
  final TextEditingController addressController = TextEditingController();
  final TextEditingController propertyTypeController = TextEditingController();
  final TextEditingController imageController = TextEditingController();
  List<Property> properties = [];

  @override
  void initState() {
    super.initState();
    loadProperties();
  }

  void loadProperties() async {
    final prefs = await SharedPreferences.getInstance();
    final List<String> propertyData = prefs.getStringList('properties') ?? [];
    setState(() {
      properties = propertyData.map((data) {
        final List<String> property = data.split(',');
        return Property(
          property[0],
          property[1],
          property[2],
          property[3],
        );
      }).toList();
    });
  }

  void saveProperty(Property property) async {
    final prefs = await SharedPreferences.getInstance();
    final propertyData =
        '${property.name},${property.address},${property.propertyType},${property.image}';
    final List<String> propertyList = prefs.getStringList('properties') ?? [];
    propertyList.add(propertyData);
    await prefs.setStringList('properties', propertyList);
  }

  void clearFields() {
    nameController.clear();
    addressController.clear();
    propertyTypeController.clear();
    imageController.clear();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('MI Casa SAS - Propiedades'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: <Widget>[
            TextField(
              controller: nameController,
              decoration: InputDecoration(labelText: 'Nombre de la propiedad'),
            ),
            TextField(
              controller: addressController,
              decoration: InputDecoration(labelText: 'Dirección'),
            ),
            TextField(
              controller: propertyTypeController,
              decoration: InputDecoration(labelText: 'Tipo de propiedad'),
            ),
            TextField(
              controller: imageController,
              decoration: InputDecoration(labelText: 'Imagen'),
            ),
            ElevatedButton(
              onPressed: () {
                final property = Property(
                  nameController.text,
                  addressController.text,
                  propertyTypeController.text,
                  imageController.text,
                );
                properties.add(property);
                saveProperty(property);
                clearFields();
                setState(() {});
              },
              child: Text('Agregar Propiedad'),
            ),
            SizedBox(height: 16),
            Text(
              'Propiedades Almacenadas',
              style: TextStyle(fontSize: 18),
            ),
            for (final property in properties)
              ListTile(
                title: Text('Nombre: ${property.name}'),
                subtitle: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Dirección: ${property.address}'),
                    Text('Tipo: ${property.propertyType}'),
                    Text('Imagen: ${property.image}'),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }
}
