import streamlit as st
from PIL import Image as im
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import numpy as np

st.set_page_config(
    page_title="Beans & Pods",
    page_icon="☕"
)

# Configuration de la page
st.markdown("<h1 class='main-header'>☕ Analyse des Ventes - Beans & Pods</h1>", unsafe_allow_html=True)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #5D4037;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .subheader {
        font-size: 1.8rem;
        color: #5D4037;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #BD632F;
        padding-bottom: 0.5rem;
    }
    .image-container {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-radius: 10px;
        overflow: hidden;
    }
    .intro-text {
        font-size: 1.1rem;
        line-height: 1.6;
        text-align: justify;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Configuration de la barre latérale pour le menu
st.sidebar.markdown("""
<div style="text-align: center; padding: 15px 10px 5px 10px; background-color: #F2F0EB; border-radius: 10px; margin-bottom: 20px;">
    <h1 style="color: #5D4037; font-size: 1.8rem; margin-bottom: 15px;">Projet IA1</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    div.row-widget.stRadio > div {
        flex-direction: column;
        gap: 10px;
    }

</style>
""", unsafe_allow_html=True)

# Menu vertical avec des boutons stylisés
menu = st.sidebar.radio(
    "",
    ["Accueil", "Visualisation", "Rapport", "Github"],
    horizontal=False
)

if menu == "Accueil":
    
    # L'introduction 
    st.markdown('<h2 class="subheader">Introduction</h2>', unsafe_allow_html=True)
    st.markdown("""
    <p class="intro-text">
    Beans & Pods, une entreprise spécialisée dans la vente de grains de café et de gousses, a récemment étendu ses opérations 
    à une plateforme en ligne avec le soutien d'Angeli VC. Ce rapport fournit une analyse détaillée des ventes par canal 
    (magasin et en ligne), par produit et par région, et propose des recommandations stratégiques pour améliorer les ventes 
    et cibler plus efficacement les clients.
    </p>
    """, unsafe_allow_html=True)
    
# L'image 
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    try:
        image = im.open("img.jpg")
        st.image(image, use_column_width=True)
    except Exception as e:
        st.warning("L'image 'img.jpg' n'a pas pu être chargée. Veuillez vérifier que le fichier existe dans le même répertoire que votre application.")
    st.markdown('</div>', unsafe_allow_html=True)
    
elif menu == "Visualisation":
    try:
        fichier = 'BeansDataSet.csv'
        data = pd.read_csv(fichier)
        pd.set_option('display.width', 100)
        pd.set_option('display.float_format', '{:.2f}'.format)

        # Afficher le DataFrame
        st.title("Analyse du Beans DataSet")
        st.subheader("Aperçu des données")
        st.dataframe(data.head())

    except FileNotFoundError:
        st.error("Erreur de lecture : Le fichier 'BeansDataSet.csv' est introuvable.")
        st.stop()

    # Aperçu des données
    st.subheader("Aperçu des données")
    st.write("Dimensions du dataset : ", data.shape)
    st.write("Nombre de lignes : ", data.shape[0])
    st.write("Nombre de colonnes : ", data.shape[1])

    # Vérification des valeurs manquantes
    st.subheader("Valeurs manquantes")
    st.write(data.isnull().sum())
    st.write(f"Nombre total de valeurs manquantes : {data.isnull().sum().sum()}")

    # Comptage par 'Channel'
    st.subheader("Analyse par Channel")
    if 'Channel' in data.columns:
        channel_count = data.groupby('Channel').size()
        st.write("Comptage des Channel :")
        st.bar_chart(channel_count)

    # Total des ventes par produit
    if {'Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino'}.issubset(data.columns):
        data['Total vente'] = data[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].sum(axis=1)
        
        st.subheader("Total des ventes")
        total_vente = data[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].sum()
        st.write(total_vente)

        # Ventes par région
        if 'Region' in data.columns:
            region_ventes = data.groupby('Region')['Total vente'].sum()
            st.subheader("Ventes par Région")
            st.bar_chart(region_ventes)

    # Statistiques descriptives
    st.subheader("Statistiques descriptives")
    st.write(data.describe())

    # Histogrammes
    st.subheader("Histogrammes")
    fig, ax = plt.subplots(figsize=(15, 10))
    data.hist(bins=15, ax=ax, layout=(3, 3), grid=True)
    st.pyplot(fig)

    try:
        fichier = 'BeansDataSet.csv'
        data = pd.read_csv(fichier)

        data.fillna(0, inplace=True)

        st.title("Graphiques de densité pour chaque colonne")

        numeric_cols = data.select_dtypes(include=['number']).columns

        if len(numeric_cols) > 0:
            fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(15, 15))
            axes = axes.flatten()

            for i, col in enumerate(numeric_cols):
                if i < len(axes):
                    sns.kdeplot(data[col], ax=axes[i], fill=True)
                    axes[i].set_title(f"Densité de {col}")

            for j in range(i + 1, len(axes)):
                fig.delaxes(axes[j])

            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("Aucune colonne numérique trouvée dans le dataset.")
    except Exception as e:
        st.error(f"Erreur lors de la génération des graphiques de densité : {e}")

    # Matrice de corrélation
    st.subheader("Matrice de corrélation")
    data_num = data.select_dtypes(include='number')
    fig, ax = plt.subplots(figsize=(15, 10))
    corr = data_num.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
    st.pyplot(fig)

    # Boîtes à moustaches
    st.subheader("Boîtes à moustaches")
    fig, ax = plt.subplots(figsize=(15, 15))
    data.plot(kind='box', layout=(3, 3), subplots=True, sharex=False, sharey=False, ax=ax)
    st.pyplot(fig)

    # Pairplot
    if 'Cappuccino' in data.columns:
        st.subheader("Pairplot (Cappuccino)")
        try:
            pairplot_fig = sns.pairplot(data, hue='Cappuccino', diag_kind="kde")
            st.pyplot(pairplot_fig.fig)
        except Exception as e:
            st.error(f"Erreur dans le pairplot (Cappuccino) : {e}")

        st.subheader("Pairplot (Arabica et Espresso)")
        try:
            pairplot_fig_2 = sns.pairplot(data, hue='Cappuccino', vars=['Arabica', 'Espresso'], diag_kind="kde")
            st.pyplot(pairplot_fig_2.fig)
        except Exception as e:
            st.error(f"Erreur dans le pairplot (Arabica et Espresso) : {e}")

elif menu == "Rapport":
    # Définition du style CSS pour le rapport
    st.markdown("""
    <style>
    .sub-header {
        color: #3A3042;
        border-bottom: 2px solid #BD632F;
        padding-bottom: 8px;
    }
    .insight-box {
        background-color: #F2F0EB;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center;'>
    <h1>Recommandations pour la Campagne Marketing</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background-color: #F7F7F7; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <p>Basé sur notre analyse approfondie des données de vente de Beans & Pods, nous avons élaboré des recommandations stratégiques pour optimiser la nouvelle campagne marketing et augmenter les revenus.</p>
    </div>
    """, unsafe_allow_html=True)

    # Recommandations par Canal
    st.markdown("<h2>Recommandations par Canal</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: #F2F0EB; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
            <h3 style="color: #3A3042; border-bottom: 2px solid #BD632F; padding-bottom: 8px;">Canal Magasin</h3>
            <p><b>Produit vedette:</b> Robusta</p>
            <p><b>Préférence observée:</b> Grains</p>
            <ul>
                <li><b>Organisation de dégustations</b> - Mettre en place des sessions de dégustation axées sur Robusta pour attirer de nouveaux clients.</li>
                <li><b>Formation du personnel</b> - Former le personnel sur les caractéristiques de Cappuccino pour stimuler ses ventes.</li>
                <li><b>Promotion croisée</b> - Offrir des remises sur Cappuccino lors de l'achat de Robusta.</li>
                <li><b>Aménagement des rayons</b> - Placer stratégiquement les produits pour encourager les achats impulsifs.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #F2F0EB; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
            <h3 style="color: #3A3042; border-bottom: 2px solid #BD632F; padding-bottom: 8px;">Canal En Ligne</h3>
            <p><b>Produit vedette:</b> Espresso</p>
            <p><b>Préférence observée:</b> Dosettes</p>
            <ul>
                <li><b>Personnalisation du site</b> - Créer des recommandations personnalisées basées sur l'historique d'achat.</li>
                <li><b>Abonnements mensuels</b> - Proposer des formules d'abonnement pour Espresso avec livraison régulière.</li>
                <li><b>Marketing par email</b> - Envoyer des promotions ciblées pour Cappuccino aux acheteurs fréquents.</li>
                <li><b>Livraison gratuite</b> - Offrir la livraison gratuite pour les commandes dépassant un certain montant.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommandations par Région
    st.markdown("<h2>Recommandations par Région</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: #F2F0EB; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
            <h3 style="color: #3A3042; border-bottom: 2px solid #BD632F; padding-bottom: 8px;">Région South</h3>
            <p><b>Produit le plus vendu:</b> Robusta</p>
            <p><b>Produit à promouvoir:</b> Cappuccino</p>
            <p><b>Canal principal:</b> Store</p>
            <ul>
                <li><b>Offres localisées</b> - Créer des offres spécifiques pour Cappuccino adaptées aux préférences régionales.</li>
                <li><b>Marketing local</b> - Collaborer avec des entreprises locales pour des promotions conjointes.</li>
                <li><b>Événements régionaux</b> - Organiser des dégustations de Robusta dans les points de vente de la région.</li>
                <li><b>Optimisation du canal</b> - Renforcer la présence dans le canal Store tout en développant l'autre canal.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #F2F0EB; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
            <h3 style="color: #3A3042; border-bottom: 2px solid #BD632F; padding-bottom: 8px;">Région North</h3>
            <p><b>Produit le plus vendu:</b> Robusta</p>
            <p><b>Produit à promouvoir:</b> Cappuccino</p>
            <p><b>Canal principal:</b> Store</p>
            <ul>
                <li><b>Offres localisées</b> - Créer des offres spécifiques pour Cappuccino adaptées aux préférences régionales.</li>
                <li><b>Marketing local</b> - Collaborer avec des entreprises locales pour des promotions conjointes.</li>
                <li><b>Événements régionaux</b> - Organiser des dégustations de Robusta dans les points de vente de la région.</li>
                <li><b>Optimisation du canal</b> - Renforcer la présence dans le canal Store tout en développant l'autre canal.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #F2F0EB; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
            <h3 style="color: #3A3042; border-bottom: 2px solid #BD632F; padding-bottom: 8px;">Région Central</h3>
            <p><b>Produit le plus vendu:</b> Robusta</p>
            <p><b>Produit à promouvoir:</b> Cappuccino</p>
            <p><b>Canal principal:</b> Online</p>
            <ul>
                <li><b>Offres localisées</b> - Créer des offres spécifiques pour Cappuccino adaptées aux préférences régionales.</li>
                <li><b>Marketing local</b> - Collaborer avec des entreprises locales pour des promotions conjointes.</li>
                <li><b>Événements régionaux</b> - Organiser des dégustations de Robusta dans les points de vente de la région.</li>
                <li><b>Optimisation du canal</b> - Renforcer la présence dans le canal Online tout en développant l'autre canal.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommandations par Produit
    st.markdown("<h2>Recommandations par Produit</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: #F2F0EB; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
            <h3 style="color: #3A3042; border-bottom: 2px solid #BD632F; padding-bottom: 8px;">Produits à forte demande</h3>
            <p><b>Produit star:</b> Robusta</p>
            <ul>
                <li><b>Mise en avant</b> - Placer Robusta en évidence dans les magasins et sur le site web.</li>
                <li><b>Éditions spéciales</b> - Lancer des éditions limitées ou des saveurs saisonnières pour Robusta.</li>
                <li><b>Programme de fidélité</b> - Offrir des points de fidélité supplémentaires pour les achats répétés.</li>
                <li><b>Témoignages clients</b> - Mettre en avant les avis positifs sur Robusta.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #F2F0EB; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
            <h3 style="color: #3A3042; border-bottom: 2px solid #BD632F; padding-bottom: 8px;">Produits à stimuler</h3>
            <p><b>Produit à développer:</b> Cappuccino</p>
            <ul>
                <li><b>Offres spéciales</b> - Proposer des remises importantes sur Cappuccino.</li>
                <li><b>Ventes groupées</b> - Créer des packs combinant Cappuccino avec Robusta.</li>
                <li><b>Éducation client</b> - Informer les clients sur les avantages uniques de Cappuccino.</li>
                <li><b>Échantillons gratuits</b> - Distribuer des échantillons de Cappuccino avec d'autres achats.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #F2F0EB; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
        <h3 style="color: #3A3042; border-bottom: 2px solid #BD632F; padding-bottom: 8px;">Associations de produits</h3>
        <p><b>Paire la plus corrélée:</b> Espresso et Latte</p>
        <ul>
            <li><b>Promotions conjointes</b> - Offrir des réductions lors de l'achat simultané de ces produits.</li>
            <li><b>Placement en magasin</b> - Placer ces produits à proximité l'un de l'autre.</li>
            <li><b>Recommandations en ligne</b> - Suggérer un produit lorsque l'autre est consulté ou ajouté au panier.</li>
            <li><b>Packs combinés</b> - Créer des offres spéciales combinant ces deux produits.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Suggestions de données supplémentaires à collecter
    st.markdown("<h2>Suggestions de Données Supplémentaires à Collecter</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #F2F0EB; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
        <p>Pour améliorer davantage l'analyse et les recommandations, nous suggérons de collecter:</p>
        <ul>
            <li><b>Données démographiques</b> - Âge, sexe, profession, revenu des clients pour mieux cibler les campagnes.</li>
            <li><b>Historique d'achat complet</b> - Fréquence d'achat, récence, valeur à vie du client pour identifier les clients fidèles.</li>
            <li><b>Feedback client</b> - Avis sur les produits, satisfaction client, préférences de goût pour améliorer l'offre.</li>
            <li><b>Comportement en ligne</b> - Pages visitées, temps passé sur le site, taux d'abandon du panier pour optimiser l'expérience utilisateur.</li>
            <li><b>Données de campagne</b> - Performance des campagnes marketing précédentes pour identifier les stratégies efficaces.</li>
            <li><b>Données temporelles</b> - Variations saisonnières des ventes pour ajuster les stocks et promotions.</li>
            <li><b>Données concurrentielles</b> - Prix et promotions des concurrents pour rester compétitif.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Plan d'action
    st.markdown("<h2>Plan d'Action et KPIs à Suivre</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #F2F0EB; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
        <h4 style="color: #3A3042;">Plan d'action à court terme (1-3 mois)</h4>
        <ol>
            <li>Lancer des promotions ciblées pour Cappuccino dans la région South.</li>
            <li>Optimiser le site web avec des recommandations personnalisées basées sur l'historique d'achat.</li>
            <li>Former le personnel de vente sur les techniques de vente croisée pour Espresso et Latte.</li>
            <li>Mettre en place un système de collecte de données clients plus détaillé.</li>
            <li>Développer des offres d'abonnement pour les produits les plus populaires.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #F2F0EB; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
        <h4 style="color: #3A3042;">KPIs à suivre</h4>
        <ul>
            <li><b>Ventes totales</b> - Augmentation des ventes globales et par canal/région/produit.</li>
            <li><b>Valeur panier moyen</b> - Évolution de la valeur moyenne des transactions.</li>
            <li><b>Taux de conversion</b> - Pourcentage de visiteurs qui finalisent un achat.</li>
            <li><b>Ventes de Cappuccino</b> - Augmentation des ventes du produit le moins performant.</li>
            <li><b>Ratio Grains/Dosettes</b> - Évolution de l'équilibre entre les types de produits.</li>
            <li><b>Taux de fidélisation</b> - Pourcentage de clients qui reviennent pour un achat ultérieur.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Conclusion
    st.markdown("<h2>Conclusion</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #F2F0EB; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
        <p>Notre analyse des données de vente de Beans & Pods a révélé plusieurs opportunités pour optimiser la stratégie marketing et augmenter les revenus. En mettant en œuvre nos recommandations personnalisées par canal, région et produit, Beans & Pods pourra:</p>
        <ul>
            <li>Augmenter les ventes des produits sous-performants</li>
            <li>Renforcer la fidélité client</li>
            <li>Optimiser l'allocation des ressources marketing</li>
            <li>Améliorer l'expérience client sur tous les canaux</li>
        </ul>
        <p>Cette approche basée sur les données permettra à Beans & Pods de maximiser son retour sur investissement marketing et de renforcer sa position sur le marché du café.</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.title("Lien vers le dépôt GitHub de l'application")
    
    st.write("Voici le lien vers le dépôt GitHub contenant le code de l'application :")
    
    st.markdown("[Lien vers le dépôt GitHub](https://github.com/rymoushe/BeansAndPods)")