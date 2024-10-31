import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def i1():
    df = pd.read_csv("users.csv")

    google_users = df[df['company'].str.contains(
        "GOOGLE", case=False, na=False)]

    sns.scatterplot(data=google_users, x="public_repos", y="followers")
    plt.xlabel("Number of Public Repositories")
    plt.ylabel("Number of Followers")
    plt.title("Google Employees: Followers vs. Number of Public Repositories")
    plt.show()


def i2():
    df = pd.read_csv("users.csv")
    df["hireable"] = df["hireable"].fillna(False)
    df['is_google'] = df['company'].str.contains(
        "GOOGLE", case=False, na=False)

    hireable_counts = df.groupby('is_google')['hireable'].mean().reset_index()
    hireable_counts['company'] = hireable_counts['is_google'].map(
        {True: "Google", False: "Other Companies"})

    plt.figure(figsize=(8, 5))
    sns.set_theme(style="whitegrid")

    bar_plot = sns.barplot(
        data=hireable_counts,
        x="company",
        y="hireable",
        palette="viridis",
        edgecolor="black"
    )

    bar_plot.set_xlabel("Company", fontsize=12)
    bar_plot.set_ylabel("Fraction Hireable", fontsize=12)
    bar_plot.set_title(
        "Hireable Status: Google vs Other Companies", fontsize=14, weight='bold')
    bar_plot.set(ylim=(0, 1))

    for p in bar_plot.patches:
        bar_plot.annotate(f'{p.get_height():.2f}',
                          (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha='center', va='baseline', fontsize=11, color='black', xytext=(0, 5),
                          textcoords='offset points')

    plt.show()


def i3():
    df = pd.read_csv("users.csv")
    df["hireable"] = df["hireable"].fillna(False)
    # Create a new category column for Google, no company, and other companies
    df['company_category'] = df['company'].apply(
        lambda x: "Google" if pd.notna(x) and "GOOGLE" in x.upper() else (
            "No Company" if pd.isna(x) else "Other Companies")
    )

    # Calculate the fraction of hireable users in each category
    hireable_counts = df.groupby('company_category')[
        'hireable'].mean().reset_index()

    plt.figure(figsize=(8, 5))
    sns.set_theme(style="whitegrid")

    bar_plot = sns.barplot(
        data=hireable_counts,
        x="company_category",
        y="hireable",
        palette="viridis",
        edgecolor="black"
    )

    bar_plot.set_xlabel("Company Category", fontsize=12)
    bar_plot.set_ylabel("Fraction Hireable", fontsize=12)
    bar_plot.set_title("Hireable Status by Company Category",
                       fontsize=14, weight='bold')
    bar_plot.set(ylim=(0, 1))

    # Annotate each bar with the fraction value
    for p in bar_plot.patches:
        bar_plot.annotate(f'{p.get_height():.2f}',
                          (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha='center', va='baseline', fontsize=11, color='black', xytext=(0, 5),
                          textcoords='offset points')

    plt.show()


def i4():
    df = pd.read_csv("users.csv")
    df["hireable"] = df["hireable"].fillna(False)

    df['company'] = df['company'].str.strip().str.upper()

    # Count the number of users in each company
    company_counts = df['company'].value_counts().reset_index()
    company_counts.columns = ['company', 'user_count']

    # Get the top 5 companies based on user counts
    top_companies = company_counts.nlargest(5, 'user_count')['company']

    # Filter the original dataframe for only these top companies
    top_company_data = df[df['company'].isin(top_companies)]

    # Calculate the fraction of hireable users for these top companies
    hireable_counts = top_company_data.groupby(
        'company')['hireable'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")

    bar_plot = sns.barplot(
        data=hireable_counts.sort_values(by='hireable', ascending=False),
        x="company",
        y="hireable",
        palette="viridis",
        edgecolor="black"
    )

    bar_plot.set_xlabel("Company", fontsize=12)
    bar_plot.set_ylabel("Fraction Hireable", fontsize=12)
    bar_plot.set_title("Hireable Status of Top 5 Companies",
                       fontsize=14, weight='bold')
    bar_plot.set(ylim=(0, 1))
    plt.xticks(rotation=45, ha='right')

    # Annotate each bar with the fraction value
    for p in bar_plot.patches:
        bar_plot.annotate(f'{p.get_height():.2f}',
                          (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha='center', va='baseline', fontsize=11, color='black', xytext=(0, 5),
                          textcoords='offset points')

    plt.tight_layout()
    plt.show()


def i5():
    df = pd.read_csv("users.csv")

    # Clean up the company column and calculate bio length
    df['company'] = df['company'].str.strip()
    df['bio_length'] = df['bio'].str.split().str.len().fillna(0)

    # Create a new column to indicate if a user has a company listed
    df['has_company'] = df['company'].notna() & (df['company'] != '')

    # Calculate average bio lengths for each group
    avg_bio_length = df.groupby('has_company')[
        'bio_length'].mean().reset_index()
    avg_bio_length['has_company'] = avg_bio_length['has_company'].map(
        {True: 'Has Company', False: 'No Company'})

    plt.figure(figsize=(8, 5))
    sns.set_theme(style="whitegrid")

    bar_plot = sns.barplot(
        data=avg_bio_length,
        x="has_company",
        y="bio_length",
        palette="pastel",
        edgecolor="black"
    )

    bar_plot.set_xlabel("Company Status", fontsize=12)
    bar_plot.set_ylabel("Average Bio Length (Words)", fontsize=12)
    bar_plot.set_title(
        "Comparison of Bio Lengths: Users with vs. without Company", fontsize=14, weight='bold')
    plt.ylim(0, avg_bio_length['bio_length'].max() + 5)

    # Annotate each bar with the average bio length
    for p in bar_plot.patches:
        bar_plot.annotate(f'{p.get_height():.1f}',
                          (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha='center', va='baseline', fontsize=11, color='black', xytext=(0, 5),
                          textcoords='offset points')

    plt.tight_layout()
    plt.show()


def i6():
    df = pd.read_csv("repositories.csv")

    company_data = df[df['company'].notna()]['public_repos']
    non_company_data = df[df['company'].isna()]['public_repos']

    averages = {
        'In Company': company_data.mean(),
        'Not In Company': non_company_data.mean()
    }

    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 5))
    sns.barplot(x=list(averages.keys()), y=list(
        averages.values()), palette="viridis")

    plt.title("Average Number of Repositories per Person")
    plt.ylabel("Average Number of Repositories")
    plt.xlabel("User Category")
    plt.ylim(0, max(averages.values()) + 1)

    for i, value in enumerate(averages.values()):
        plt.text(i, value + 0.1, f"{value:.3f}", ha='center')

    plt.show()


def i7():
    repos_df = pd.read_csv("repositories.csv")
    repos_df['created_at'] = pd.to_datetime(repos_df['created_at'])

    rust_repos = repos_df[repos_df['language'] == 'Rust']
    rust_repos_count = rust_repos.groupby(
        rust_repos['created_at'].dt.to_period('M')).size().cumsum()

    plt.figure(figsize=(10, 6))
    rust_repos_count.plot(kind='line', marker='o', color='orange')

    plt.title("Cumulative Number of Rust Repositories Over Time")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Number of Repositories")
    plt.xticks(rotation=45)
    plt.grid(True)

    plt.show()


def i8():
    repos_df = pd.read_csv("repositories.csv")
    repos_df['created_at'] = pd.to_datetime(repos_df['created_at'])

    rust_repos = repos_df[repos_df['language'] == 'Rust']
    js_repos = repos_df[repos_df['language'] == 'JavaScript']

    rust_cumulative = rust_repos.groupby(
        rust_repos['created_at'].dt.to_period('M')).size().cumsum()
    js_cumulative = js_repos.groupby(
        js_repos['created_at'].dt.to_period('M')).size().cumsum()

    plt.figure(figsize=(10, 6))
    rust_cumulative.plot(kind='line', marker='o', color='orange', label='Rust')
    js_cumulative.plot(kind='line', marker='o',
                       color='blue', label='JavaScript')

    plt.title("Cumulative Number of Rust and JavaScript Repositories Over Time")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Number of Repositories")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()

    plt.show()


def i9():
    repos_df = pd.read_csv("repositories.csv")
    repos_df['created_at'] = pd.to_datetime(repos_df['created_at'])

    rust_repos = repos_df[repos_df['language'] == 'TypeScript']
    js_repos = repos_df[repos_df['language'] == 'JavaScript']

    rust_yearly = rust_repos.groupby(rust_repos['created_at'].dt.year).size()
    js_yearly = js_repos.groupby(js_repos['created_at'].dt.year).size()

    plt.figure(figsize=(10, 6))
    rust_yearly.plot(kind='bar', color='orange',
                     label='TypeScript', width=0.4, position=1)
    js_yearly.plot(kind='bar', color='blue',
                   label='JavaScript', width=0.4, position=0)

    plt.title("Yearly Count of TypeScript and JavaScript Repositories Created")
    plt.xlabel("Year")
    plt.ylabel("Number of Repositories Created")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.legend()

    plt.show()


def i10():
    users_df = pd.read_csv("users.csv")
    repos_df = pd.read_csv("repositories.csv")

    repos_df['created_at'] = pd.to_datetime(repos_df['created_at'])
    repos_df['year'] = repos_df['created_at'].dt.year

    google_users = users_df[users_df['company'].str.contains(
        "Google", case=False, na=False)]
    google_repos = repos_df[repos_df['login'].isin(google_users['login'])]

    language_counts = google_repos.groupby(
        ['year', 'language']).size().unstack(fill_value=0)

    plt.figure(figsize=(16, 8))
    language_counts.plot(kind='bar', stacked=True, cmap='tab20')

    plt.title("Different Programming Languages Used by Google Over the Years")
    plt.xlabel("Year")
    plt.ylabel("Number of Repositories Created")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')

    plt.legend(title='Language', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout(pad=2.0)
    plt.show()


def i12():
    users_df = pd.read_csv("users.csv")
    repos_df = pd.read_csv("repositories.csv")

    google_users = users_df[users_df['company'].str.contains(
        "Google", case=False, na=False)]
    google_repos = repos_df[repos_df['login'].isin(google_users['login'])]

    total_repos = len(google_repos)
    language_counts = google_repos['language'].value_counts()

    language_percentages = (language_counts / total_repos) * 100
    language_percentages = language_percentages.fillna(0)

    plt.figure(figsize=(10, 6))
    language_percentages.plot(kind='bar', color='skyblue')
    plt.title('Percentage of Programming Languages Used by Google Employees')
    plt.xlabel('Programming Languages')
    plt.ylabel('Percentage of Repositories (%)')
    plt.xticks(rotation=45)
    plt.axhline(0, color='grey', linewidth=0.8)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


i12()
