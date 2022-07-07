plugins {
    kotlin("jvm") version "1.5.31"
}

group = "org.example"
version = "1.0-SNAPSHOT"
val atalaPrismVersion = System.getenv("ATALA_PRISM_VERSION")
val dockerSdkJarsDir = "/home/atala_prism_sdk"

repositories {
    mavenCentral()
    mavenLocal()
    google()
    maven("https://plugins.gradle.org/m2/")
    // Required for Kotlin coroutines that support new memory management mode
    maven {
        url = uri("https://maven.pkg.jetbrains.space/public/p/kotlinx-coroutines/maven")
    }
    maven {
        url = uri("https://maven.pkg.github.com/input-output-hk/atala-prism-sdk")
        credentials {
            username = System.getenv("ATALA_GITHUB_ACTOR")
            password = System.getenv("ATALA_GITHUB_TOKEN")
        }
    }
}

dependencies {
    implementation(kotlin("stdlib"))
    // needed for cryptography primitives implementation
    implementation("io.iohk.atala:prism-crypto:$atalaPrismVersion")
    // needed to deal with DIDs
    implementation("io.iohk.atala:prism-identity:$atalaPrismVersion")
    // needed to deal with credentials
    implementation("io.iohk.atala:prism-credentials:$atalaPrismVersion")
    // needed to interact with PRISM Node service
    implementation("io.iohk.atala:prism-api:$atalaPrismVersion")
    // needed for the credential content, bring the latest version
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.2.2")
    // needed for dealing with dates, bring the latest version
    implementation("org.jetbrains.kotlinx:kotlinx-datetime:0.2.1")
    // DIDComm v2 JVM from https://github.com/sicpa-dlab/didcomm-jvm
    implementation("org.didcommx:didcomm:0.3.0")
    // Peer DID implementation from https://github.com/sicpa-dlab/peer-did-jvm
    implementation("org.didcommx:peerdid:0.3.0")
}

// try using regular task.create because we don't need  a reference, also after that try using .register becuase we don't need eager creating

val copyToJypiterClassPath by tasks.creating(Copy::class) {
    from(configurations.runtimeClasspath.get().resolve())
    into(layout.buildDirectory.dir(dockerSdkJarsDir))
    dependsOn(tasks.build)
}

tasks.register("saveAtalaSdkDependencies") {
    doLast {
        var sdkDependencies = ""
        configurations.runtimeClasspath.get().resolve().forEach {
            sdkDependencies += "@file:DependsOn(\"$dockerSdkJarsDir/${it.name}\")\n"
        }
        File(projectDir, "atala_sdk_dependencies.txt").writeText(sdkDependencies)
    }
}

tasks.register("printPath") {
    configurations.runtimeClasspath.get().resolve().forEach { file ->
        println(file.name)
    }
}
