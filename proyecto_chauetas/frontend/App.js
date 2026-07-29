import React, { useEffect, useState } from 'react';
import { SafeAreaView, View, FlatList, StyleSheet } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Provider as PaperProvider, DefaultTheme, Appbar, TextInput, Button, Card, Text } from 'react-native-paper';
import { LinearGradient } from 'expo-linear-gradient';

export default function App() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState('');
  const [quantity, setQuantity] = useState('1');
  const [token, setToken] = useState(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [logged, setLogged] = useState(false);

  const API_BASE = 'http://10.0.2.2:8000/api'; // Android emulator; use http://localhost:8000 on some setups

  useEffect(() => {
    (async () => {
      const t = await AsyncStorage.getItem('token');
      if (t) {
        setToken(t);
        setLogged(true);
        fetchItems(t);
      }
    })();
  }, []);

  const theme = {
    ...DefaultTheme,
    roundness: 10,
    colors: {
      ...DefaultTheme.colors,
      primary: '#00FFC2',
      accent: '#7AE7FF',
      background: '#081028',
      surface: '#0f1b2b',
      text: '#E6FBFF',
    },
  };

  const fetchItems = async (tkn) => {
    try {
      const headers = tkn || token ? { 'Authorization': `Bearer ${tkn || token}` } : {};
      const res = await fetch(`${API_BASE}/items/`, { headers });
      if (res.status === 401) {
        setItems([]);
        setLogged(false);
        return;
      }
      const data = await res.json();
      setItems(data);
    } catch (e) {
      console.error(e);
    }
  };

  const addItem = async () => {
    if (!name) return;
    try {
      const headers = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;
      const res = await fetch(`${API_BASE}/items/`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ name, quantity: parseInt(quantity || '0') })
      });
      if (res.status === 401) {
        setLogged(false);
        return;
      }
      setName('');
      setQuantity('1');
      fetchItems();
    } catch (e) {
      console.error(e);
    }
  };

  const doLogin = async () => {
    try {
      const res = await fetch(`${API_BASE}/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      if (!res.ok) {
        return;
      }
      const data = await res.json();
      await AsyncStorage.setItem('token', data.access);
      setToken(data.access);
      setLogged(true);
      fetchItems(data.access);
    } catch (e) {
      console.error(e);
    }
  };

  const doLogout = async () => {
    await AsyncStorage.removeItem('token');
    setToken(null);
    setLogged(false);
    setItems([]);
  };

  return (
    <PaperProvider theme={theme}>
      <LinearGradient colors={["#061028","#081a34"]} style={{flex:1}}>
        <SafeAreaView style={styles.container}>
          <Appbar.Header elevated style={{backgroundColor:'transparent'}}>
            <Appbar.Content title="Inventario - Cecytem Tecámac" subtitle="Panel" />
          </Appbar.Header>

          <View style={styles.content}>
            {!logged ? (
              <Card style={styles.card}>
                <Card.Content>
                  <Text style={styles.hint}>Inicia sesión para gestionar el inventario</Text>
                  <TextInput label="Usuario" value={username} onChangeText={setUsername} style={styles.input} mode="outlined" />
                  <TextInput label="Contraseña" secureTextEntry value={password} onChangeText={setPassword} style={styles.input} mode="outlined" />
                  <Button mode="contained" onPress={doLogin} style={styles.button}>Iniciar sesión</Button>
                </Card.Content>
              </Card>
            ) : (
              <Card style={styles.card}>
                <Card.Content>
                  <Text style={styles.hint}>Añadir nuevo ítem</Text>
                  <TextInput label="Nombre" value={name} onChangeText={setName} style={styles.input} mode="outlined" />
                  <TextInput label="Cantidad" value={quantity} onChangeText={setQuantity} keyboardType="numeric" style={styles.input} mode="outlined" />
                  <Button mode="contained" onPress={addItem} style={styles.button}>Agregar</Button>
                  <Button mode="text" onPress={doLogout} style={{marginTop:8}}>Cerrar sesión</Button>
                </Card.Content>
              </Card>
            )}

            <FlatList
              data={items}
              keyExtractor={(item) => item.id.toString()}
              contentContainerStyle={{paddingBottom:80}}
              renderItem={({ item }) => (
                <Card style={styles.itemCard}>
                  <Card.Content style={{flexDirection:'row',justifyContent:'space-between',alignItems:'center'}}>
                    <Text style={{color:theme.colors.text,fontSize:16}}>{item.name}</Text>
                    <Text style={{color:theme.colors.accent,fontWeight:'700'}}>{item.quantity}</Text>
                  </Card.Content>
                </Card>
              )}
            />
          </View>
        </SafeAreaView>
      </LinearGradient>
    </PaperProvider>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: '#fff' },
  title: { fontSize: 20, fontWeight: 'bold', marginBottom: 12 },
  form: { marginBottom: 12 },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 8, marginBottom: 8 },
  item: { padding: 8, borderBottomWidth: 1, borderBottomColor: '#eee' },
  itemText: { fontSize: 16 }
});
