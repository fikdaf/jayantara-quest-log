import React from "react";
import { SafeAreaView, Text, View, StyleSheet } from "react-native";

export default function App() {
  return (
    <SafeAreaView style={styles.root}>
      <View style={styles.content}>
        <Text style={styles.title}>JAYANTARA</Text>
        <Text style={styles.subtitle}>Nihongo Master-Kit</Text>
        <Text style={styles.status}>Quest progress is ready to connect to @jayantara/core.</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1 },
  content: { flex: 1, alignItems: "center", justifyContent: "center", padding: 24 },
  title: { fontSize: 32, fontWeight: "800" },
  subtitle: { fontSize: 18, marginTop: 8 },
  status: { marginTop: 24, textAlign: "center" }
});
