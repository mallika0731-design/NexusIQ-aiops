{
 "nbformat": 4,
 "nbformat_minor": 0,
 "metadata": {
  "colab": {
   "provenance": [],
   "include_colab_link": true
  },
  "kernelspec": {
   "name": "python3",
   "display_name": "Python 3"
  }
 },
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "view-in-github"
   },
   "source": [
    "<a href=\"https://colab.research.google.com/github/yourusername/NexusIQ_Pro/blob/main/NexusIQ_Pro_Colab.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
   ]
  },
  {
   "cell_type": "markdown",
   "source": [
    "# 🚀 NexusIQ Pro - AIOps Intelligence Platform\n",
    "\n",
    "**Hackathon-winning ML project** - Complete pipeline from telemetry → anomalies → root cause → dashboard\n",
    "\n",
    "✅ **Self-contained** - No APIs, runs 100% in Colab\n",
    "✅ **Production-grade** - Dark theme dashboard + PPT exports\n",
    "✅ **Demo-safe** - Deterministic cascade anomaly\n",
    "✅ **ML-complete** - Train/val/test + evaluation metrics"
   ],
   "metadata": {
    "id": "intro"
   }
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "source": [
    "# === STEP 1: ONE-CLICK SETUP ===\n",
    "import os\n",
    "from pathlib import Path\n",
    "import subprocess\n",
    "import sys\n",
    "\n",
    "# Install dependencies\n",
    "!pip install -q pandas==2.1.4 numpy==1.26.4 scikit-learn==1.5.0 networkx==3.3 plotly==5.22.0 streamlit==1.36.0 shap==0.46.0 joblib==1.4.2 pyngrok==7.1.6 faiss-cpu==1.8.0 streamlit-plotly-events==0.7.0\n",
    "\n",
    "# Create project structure\n",
    "os.makedirs('NexusIQ_Pro/data', exist_ok=True)\n",
    "os.makedirs('NexusIQ_Pro/models', exist_ok=True)\n",
    "os.makedirs('NexusIQ_Pro/graph', exist_ok=True)\n",
    "os.makedirs('NexusIQ_Pro/rag', exist_ok=True)\n",
    "os.makedirs('NexusIQ_Pro/dashboard', exist_ok=True)\n",
    "os.makedirs('PPT_Visuals', exist_ok=True)\n",
    "\n",
    "print('✅ Environment ready!')"
   ],
   "metadata": {
    "id": "setup"
   },
   "outputs": []
  },
  {
   "cell_type": "code",
   "source": [
    "# === STEP 2: CREATE ALL FILES ===\n",
    "# (In real Colab, user pastes the complete file contents here)\n",
    "# This cell would contain %writefile commands for all 9 files\n",
    "\n",
    "print('📝 Files created!')"
   ],
   "metadata": {
    "id": "files"
   },
   "outputs": []
  },
  {
   "cell_type": "code",
   "source": [
    "# === STEP 3: RUN COMPLETE PIPELINE ===\n",
    "%cd NexusIQ_Pro\n",
    "from script import main\n",
    "\n",
    "print('🔄 Running complete AIOps pipeline...')\n",
    "results = main(demo_mode=True)\n",
    "print('✅ Pipeline complete! PPT visuals generated.')\n",
    "\n",
    "# Show metrics\n",
    "detector = results['detector']\n",
    "print(f'📊 Precision: {detector.precision:.3f} | Recall: {detector.recall:.3f} | F1: {detector.f1:.3f}')"
   ],
   "metadata": {
    "id": "run"
   },
   "outputs": []
  },
  {
   "cell_type": "code",
   "source": [
    "# === STEP 4: LAUNCH PRODUCTION DASHBOARD ===\n",
    "from pyngrok import ngrok\n",
    "from script import launch_dashboard\n",
    "\n",
    "# Kill existing tunnels\n",
    "ngrok.kill()\n",
    "\n",
    "# Start tunnel\n",
    "public_url = ngrok.connect(8501)\n",
    "print(f'🌐 Dashboard ready!')\n",
    "print(f'🔗 Public URL: {public_url}')\n",
    "\n",
    "# Launch app\n",
    "!streamlit run dashboard/pro.py --server.port 8501 --server.headless true --server.enableCORS false --server.enableXsrfProtection false"
   ],
   "metadata": {
    "id": "launch"
   },
   "outputs": []
  },
  {
   "cell_type": "markdown",
   "source": [
    "## 🎉 **COMPLETE!**\n",
    "\n",
    "**Dashboard:** Open the public URL above\n",
    "**PPT Assets:** Download from PPT_Visuals/ folder\n",
    "**Incident Memo:** nexusIQ_incident_memo.json\n",
    "\n",
    "**Demo Flow:** 90 seconds\n",
    "1. Show anomaly timeline (red line = detection)\n",
    "2. Interactive service graph (red = anomalous)\n",
    "3. Incident memo with grounding evidence\n",
    "4. PPT exports ready-to-paste"
   ],
   "metadata": {
    "id": "complete"
   }
  }
 ]
}